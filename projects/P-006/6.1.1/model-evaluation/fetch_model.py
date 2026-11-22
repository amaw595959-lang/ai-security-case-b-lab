"""Fetch the pinned public model artifact. This script never handles prompts."""

import hashlib
import json
import sys
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import Request, urlopen


PLAN_PATH = Path(__file__).with_name("plan.json")
REGISTRY = "https://registry-1.docker.io"


def download(artifact_dir: Path) -> None:
    spec = json.loads(PLAN_PATH.read_text(encoding="utf-8"))["model"]
    repository = spec["repository"]
    query = urlencode({"service": "registry.docker.io", "scope": f"repository:{repository}:pull"})
    with urlopen(f"https://auth.docker.io/token?{query}", timeout=30) as response:
        token = json.load(response)["token"]

    def fetch(path: str, *, accept: str = "application/octet-stream"):
        request = Request(f"{REGISTRY}/v2/{repository}/{path}", headers={"Accept": accept})
        request.add_unredirected_header("Authorization", f"Bearer {token}")
        return urlopen(request, timeout=60)

    digest = spec["manifest_digest"]
    with fetch(f"manifests/{digest}", accept="application/vnd.oci.image.manifest.v1+json") as response:
        manifest_raw = response.read()
    if f"sha256:{hashlib.sha256(manifest_raw).hexdigest()}" != digest:
        raise ValueError("Model manifest hash mismatch")
    manifest = json.loads(manifest_raw)

    expected = f"sha256:{spec['weights_sha256']}"
    layer = next(layer for layer in manifest["layers"] if layer["digest"] == expected)
    if layer["mediaType"] != "application/vnd.docker.ai.gguf.v3" or layer["size"] != spec["weights_bytes"]:
        raise ValueError("Pinned layer does not match the expected GGUF")

    config_digest = manifest["config"]["digest"]
    with fetch(f"blobs/{config_digest}") as response:
        config_raw = response.read()
    if f"sha256:{hashlib.sha256(config_raw).hexdigest()}" != config_digest:
        raise ValueError("Model config hash mismatch")

    artifact_dir.mkdir(mode=0o700, parents=True, exist_ok=True)
    output = artifact_dir / "model.gguf"
    if output.exists():
        raise FileExistsError(f"Choose a new artifact directory: {output}")
    temporary = artifact_dir / "model.gguf.part"
    checksum = hashlib.sha256()
    size = 0
    with fetch(f"blobs/{expected}") as response, temporary.open("xb") as destination:
        while chunk := response.read(1024 * 1024):
            size += len(chunk)
            if size > layer["size"]:
                raise ValueError("Model blob exceeds its manifest size")
            checksum.update(chunk)
            destination.write(chunk)
    if checksum.hexdigest() != spec["weights_sha256"] or size != layer["size"]:
        raise ValueError("Model blob hash or size mismatch")
    # The model is public and read by an unprivileged user in a rootless container.
    temporary.chmod(0o444)
    temporary.rename(output)

    print(json.dumps({
        "registry": REGISTRY,
        "repository": repository,
        "manifest_digest": digest,
        "manifest": manifest,
        "config": json.loads(config_raw),
        "weights_sha256": checksum.hexdigest(),
        "weights_bytes": size,
    }, indent=2))


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("Usage: python -B fetch_model.py ARTIFACT_DIR")
    download(Path(sys.argv[1]))
