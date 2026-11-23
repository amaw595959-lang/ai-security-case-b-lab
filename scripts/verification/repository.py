"""Read tracked content without following paths out of the checkout."""

import hashlib
import posixpath
import subprocess
from pathlib import Path


P006 = "projects/P-006"
DESIGN = f"{P006}/6.1.1"
DEMO = f"{DESIGN}/req07-http-integration"
COMPARISON = f"{P006}/6.1.3/phase-a-multi-model"
PREVIEW = f"{P006}/6.1.4/phase-b-req07"
EVENTS = f"{P006}/6.1.5/phase-c-req08"
PIN = "0666e59d26a4d056e0bacee41742486badd71cf8"


def git(root, *args):
    return subprocess.check_output(["git", "-C", str(root), *args], stderr=subprocess.PIPE)


def sha256(data):
    return hashlib.sha256(data).hexdigest()


def digest(path):
    with path.open("rb") as handle:
        return hashlib.file_digest(handle, "sha256").hexdigest()


def relative(base, pathname):
    if not pathname or pathname.startswith("/") or "\\" in pathname or "\x00" in pathname:
        raise ValueError("Expected a relative repository path")
    name = posixpath.normpath(posixpath.join(base, pathname))
    if name in {".", ".."} or name.startswith("../") or ".git" in name.split("/"):
        raise ValueError("Path leaves the repository content")
    return name


class Repository:
    def __init__(self, root, names=None):
        self.root = Path(root).resolve()
        if names is None:
            output = git(self.root, "ls-files", "--cached", "--others", "--exclude-standard", "-z")
            names = output.decode().split("\x00")
        self.names = frozenset(set(names) - {""})

    def path(self, name, *, directory=False):
        path = self.root / relative("", name)
        try:
            resolved = path.resolve()
        except RuntimeError as error:
            raise ValueError("Repository path cannot be resolved") from error
        if resolved != path:
            raise ValueError("Symbolic links are outside repository verification")
        if name in self.names and path.is_file():
            return path
        if directory and path.is_dir() and any(entry.startswith(f"{name}/") for entry in self.names):
            return path
        raise FileNotFoundError(name)

    def text(self, name):
        return self.path(name).read_text(encoding="utf-8")
