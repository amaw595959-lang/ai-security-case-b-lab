"""Run the pinned T01/T02 requests through one offline llama.cpp container."""

import argparse
import hashlib
import json
import platform
import subprocess
import sys
import time
from datetime import UTC, datetime
from pathlib import Path
from uuid import uuid4


HERE = Path(__file__).resolve().parent
PRACTICE = HERE.parent / "practice-lab"
FIXTURE = PRACTICE / "fixtures" / "case-b.json"
ORACLE = PRACTICE / "model_oracle.py"
PLAN_FILE = HERE / "plan.json"
PLAN = json.loads(PLAN_FILE.read_text(encoding="utf-8"))
FRESH_CASES = ("T01-A", "T01-B", "T02-A", "T02-B", "T02-C")
FOLLOWUP = "T01-C"
MODEL_IN_CONTAINER = "/models/model.gguf"


def utc_now():
    return datetime.now(UTC).isoformat(timespec="milliseconds")


def sha256_file(path):
    with path.open("rb") as handle:
        return hashlib.file_digest(handle, "sha256").hexdigest()


def checked_fixtures():
    if sha256_file(FIXTURE) != PLAN["fixture_sha256"] or sha256_file(ORACLE) != PLAN["oracle_sha256"]:
        raise ValueError("Fixture or oracle differs from the reviewed practice lab")
    fixtures = json.loads(FIXTURE.read_text(encoding="utf-8"))
    if fixtures["fixture_version"] != PLAN["fixture_version"] or fixtures["lab"] != PLAN["lab"]:
        raise ValueError("Wrong fixture version or lab")
    if tuple(PLAN["initial_order"]) != FRESH_CASES or PLAN["attempts_per_case"] != 1:
        raise ValueError("Unexpected attempt order or count")
    return fixtures


def variant_inputs(fixtures, case):
    scenario, variant_id = case.split("-")
    variants = fixtures[scenario]["variants"]
    return next(item for item in variants if item["id"] == variant_id)


def first_message(fixtures, case):
    scenario = case.split("-")[0]
    notice = fixtures["notice"]
    variant = variant_inputs(fixtures, case)
    notes = notice["note_block"].splitlines()
    # The note block and ordered field map come from the hash-checked fixture.
    fields = notice["fields"]
    if len(notes) != len(fields):
        raise ValueError("Fixture note block no longer matches its fields")
    supplied_notes = [
        note for field, note in zip(fields, notes, strict=True) if field not in variant["omit_fields"]
    ]
    request = variant["request"] if scenario == "T01" else fixtures[scenario]["request"]
    return {"role": "user", "content": "\n\n".join((notice["policy_line"], "\n".join(supplied_notes), request))}


def docker(*args, **options):
    return subprocess.run(
        ["docker", *args], capture_output=True, encoding="utf-8", timeout=options.pop("timeout", 30), **options
    )


def docker_output(*args):
    result = docker(*args, check=True)
    return (result.stdout + result.stderr).strip()


def request(endpoint, body=None):
    if PLAN["route"] != "http://127.0.0.1:8080":
        raise ValueError("Expected the container's loopback-only model route")
    command = [
        "exec", "-i", PLAN["container"], "/usr/bin/curl", "-q",
        "--silent", "--show-error", "--max-time", "100", "--noproxy", "127.0.0.1",
        "--write-out", "\n%{http_code}",
    ]
    if body is not None:
        command.extend(("--header", "Content-Type: application/json", "--data-binary", "@-"))
    command.append(PLAN["route"] + endpoint)
    started_at = utc_now()
    result = docker(*command, input=body, timeout=110)
    raw_body, separator, status = result.stdout.rpartition("\n")
    return {
        "started_at": started_at,
        "finished_at": utc_now(),
        "endpoint": endpoint,
        "curl_exit": result.returncode,
        "http_status": int(status) if separator and status.isdigit() else None,
        "body": raw_body if separator and status.isdigit() else result.stdout,
        "stderr": result.stderr,
    }


def successful(record):
    return record.get("curl_exit") == 0 and record.get("http_status") == 200


def request_json(endpoint):
    record = request(endpoint)
    if not successful(record):
        raise RuntimeError(f"{endpoint} unavailable: {record['http_status']} {record['stderr']}")
    return json.loads(record["body"])


def start_lab(artifact_dir):
    model_file = Path(artifact_dir).resolve() / "model.gguf"
    if sha256_file(model_file) != PLAN["model"]["weights_sha256"]:
        raise ValueError("Wrong model weights")
    container_id = docker_output(
        "run", "--detach", "--pull", "never", "--platform", PLAN["platform"],
        "--name", PLAN["container"], "--label", f"caseb.lab={PLAN['lab']}",
        "--network", "none", "--read-only", "--cap-drop", "ALL", "--security-opt",
        "no-new-privileges", "--log-driver", "none",
        "--mount", f"type=bind,src={model_file},dst={MODEL_IN_CONTAINER},readonly",
        PLAN["image"], *PLAN["server_args"],
    )
    print(container_id, flush=True)
    for _ in range(45):
        result = request("/health")
        if successful(result):
            print("Local model health:", result["body"])
            return
        running = docker_output("container", "inspect", "--format", "{{.State.Running}}", container_id)
        if running != "true":
            raise RuntimeError("Model container exited before health check. Inspect it before retrying.")
        time.sleep(1)
    raise RuntimeError("The isolated model did not become ready")


def verify_runtime():
    state = json.loads(docker_output("container", "inspect", PLAN["container"]))[0]
    image = json.loads(docker_output("image", "inspect", PLAN["image"]))[0]
    host = state["HostConfig"]
    config = state["Config"]
    mounts = [{key: mount[key] for key in ("Type", "Destination", "RW")} for mount in state["Mounts"]]
    isolation = {
        "network_mode": host["NetworkMode"],
        "networks": sorted(state["NetworkSettings"]["Networks"]),
        "port_bindings": host["PortBindings"],
        "read_only_root": host["ReadonlyRootfs"],
        "log_driver": host["LogConfig"]["Type"],
        "cap_drop": host["CapDrop"],
        "security_options": host["SecurityOpt"],
        "mounts": mounts,
    }
    if (
        isolation["network_mode"] != "none" or isolation["networks"] != ["none"]
        or isolation["port_bindings"] or not isolation["read_only_root"]
        or isolation["log_driver"] != "none" or isolation["cap_drop"] != ["ALL"]
        or isolation["security_options"] != ["no-new-privileges"]
        or mounts != [{"Type": "bind", "Destination": MODEL_IN_CONTAINER, "RW": False}]
    ):
        raise ValueError(f"Unexpected container isolation: {isolation}")
    if (
        state["Image"] != image["Id"] or PLAN["image"] not in image["RepoDigests"]
        or f"{image['Os']}/{image['Architecture']}" != PLAN["platform"]
        or config["Labels"].get("caseb.lab") != PLAN["lab"]
        or config["Entrypoint"] != ["/app/llama-server"] or config["Cmd"] != PLAN["server_args"]
    ):
        raise ValueError("Container image, lab label, or server arguments differ from the plan")

    weights = docker_output("exec", PLAN["container"], "sha256sum", MODEL_IN_CONTAINER).split()[0]
    version = docker_output("exec", PLAN["container"], "/app/llama-server", "--version")
    if weights != PLAN["model"]["weights_sha256"] or PLAN["engine_build"] not in version:
        raise ValueError("Loaded model artifact or Llama engine build differs from the plan")

    models = request_json("/v1/models")
    props = request_json("/props")
    if (
        [entry["id"] for entry in models["data"]] != [PLAN["model"]["alias"]]
        or props["model_path"] != MODEL_IN_CONTAINER or props["total_slots"] != 1
        or props["default_generation_settings"]["n_ctx"] != 2048
    ):
        raise ValueError("Live model mapping or context settings differ from the plan")
    return {
        "verified_at": utc_now(),
        "route": PLAN["route"],
        "transport": "docker exec with curl inside the model container",
        "engine": version,
        "image": PLAN["image"],
        "image_id": image["Id"],
        "platform": PLAN["platform"],
        "server_args": config["Cmd"],
        "weights_sha256": weights,
        "isolation": isolation,
        "reported_models": models,
        "reported_props": props,
    }


def write_json(path, data):
    with path.open("x", encoding="utf-8") as handle:
        json.dump(data, handle, indent=2, ensure_ascii=False)
        handle.write("\n")


def read_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def capture(run, run_id, case, messages):
    attempt_dir = run / case
    attempt_dir.mkdir(mode=0o700)
    call = {"model": PLAN["model"]["alias"], "messages": messages, **PLAN["generation"]}
    request_path = attempt_dir / "request.json"
    write_json(request_path, call)
    body = request_path.read_text(encoding="utf-8")
    write_json(attempt_dir / "attempt.json", {
        "run_id": run_id,
        "attempt_id": str(uuid4()),
        "case": case,
        "conversation": "T01-A" if case == FOLLOWUP else case,
        "actor": "analyst-fixture",
        "created_at": utc_now(),
        "request_sha256": sha256_file(request_path),
    })
    for endpoint, filename in (("/apply-template", "template.json"), ("/v1/chat/completions", "response.json")):
        try:
            record = request(endpoint, body)
        except subprocess.TimeoutExpired as error:
            record = {
                "endpoint": endpoint, "error": "transport timeout", "finished_at": utc_now(),
                "partial_stdout": (error.stdout or b"").decode("utf-8", errors="replace"),
                "partial_stderr": (error.stderr or b"").decode("utf-8", errors="replace"),
            }
        write_json(attempt_dir / filename, record)
    print(f"{case} captured, HTTP status {record.get('http_status')}")


def run_initial(run):
    fixtures = checked_fixtures()
    runtime = verify_runtime()
    run.mkdir(mode=0o700)
    run_id = str(uuid4())
    write_json(run / "run.json", {
        "run_id": run_id,
        "planned_at": utc_now(),
        "base_commit": PLAN["base_commit"],
        "adapter_commit": subprocess.check_output(
            ["git", "-C", str(HERE), "rev-parse", "HEAD"], text=True
        ).strip(),
        "adapter_sha256": sha256_file(Path(__file__)),
        "plan_sha256": sha256_file(PLAN_FILE),
        "fixture_sha256": PLAN["fixture_sha256"],
        "oracle_sha256": PLAN["oracle_sha256"],
        "plan": PLAN,
        "python": platform.python_version(),
        "machine": platform.machine(),
        "runtime": runtime,
        "scope": "Local-only model behavior. Synthetic fixture, workspace evidence, repository review.",
    })
    for case in FRESH_CASES:
        capture(run, run_id, case, [first_message(fixtures, case)])


def model_reply(run, case):
    response_path = run / case / "response.json"
    if not response_path.is_file():
        return None, False
    record = read_json(response_path)
    if not successful(record):
        return None, False
    try:
        raw = json.loads(record["body"])
        choice = raw["choices"][0]
        message = choice["message"]
        text = message["content"]
        complete = (
            raw["model"] == PLAN["model"]["alias"] and message["role"] == "assistant"
            and choice["finish_reason"] == "stop" and isinstance(text, str) and bool(text.strip())
        )
    except (json.JSONDecodeError, KeyError, IndexError, TypeError):
        return None, False
    return text if isinstance(text, str) else None, complete


def reviewed_label(run, annotations, case):
    review = annotations["cases"].get(case)
    if review is not None and sha256_file(run / case / "response.json") != review["response_file_sha256"]:
        raise ValueError(f"Review is tied to a different response for {case}")
    return review


def follow_up(run, annotations):
    fixtures = checked_fixtures()
    run_record = check_review_run(run, annotations)
    if (run / "followup.json").exists() or (run / FOLLOWUP).exists():
        raise FileExistsError("The follow-up already has a record in this run")
    review = reviewed_label(run, annotations, "T01-A")
    reply, complete = model_reply(run, "T01-A")
    if complete and not review:
        raise ValueError("Annotate the complete T01-A reply before choosing the follow-up")
    first_review = review["annotation"] if review else {}
    qualifies = (
        complete and reply and first_review.get("complete", True)
        and first_review.get("kind") == "audience_question"
    )
    disposition = "ATTEMPTED" if qualifies else "NOT_TESTED"
    explanation = (
        "T01-A asked which audience to use before drafting."
        if qualifies else "No complete T01-A audience clarification before drafting was established."
    )
    if qualifies:
        verify_runtime()
        original = read_json(run / "T01-A" / "request.json")["messages"]
        request_text = variant_inputs(fixtures, FOLLOWUP)["request"]
        messages = [*original, {"role": "assistant", "content": reply}, {"role": "user", "content": request_text}]
        capture(run, run_record["run_id"], FOLLOWUP, messages)
    write_json(run / "followup.json", {
        "run_id": run_record["run_id"], "case": FOLLOWUP, "at": utc_now(),
        "disposition": disposition, "reason": explanation,
    })
    print(f"{FOLLOWUP} {disposition} {explanation}")


def check_review_run(run, annotations):
    run_record = read_json(run / "run.json")
    if run_record["plan_sha256"] != sha256_file(PLAN_FILE):
        raise ValueError("Run used a different evaluation plan")
    if annotations["run_id"] != run_record["run_id"]:
        raise ValueError("Review is tied to a different run")
    return run_record


def score(run, annotations):
    fixtures = checked_fixtures()
    run_record = check_review_run(run, annotations)
    sys.path.insert(0, str(PRACTICE))
    from model_oracle import ReplyExpectation, ReplyReview, evaluate_reply

    results = {}
    for case in (*FRESH_CASES, FOLLOWUP):
        if case == FOLLOWUP and not (run / case).exists():
            followup_path = run / "followup.json"
            disposition = read_json(followup_path)["disposition"] if followup_path.exists() else None
            results[case] = "NOT_TESTED" if disposition == "NOT_TESTED" else "INCONCLUSIVE"
            continue
        variant = variant_inputs(fixtures, case)
        rubric = variant["expectation"]
        fields = fixtures["notice"]["fields"]
        expectation = ReplyExpectation(
            kind=rubric["kind"],
            allowed_facts={key: fields[key] for key in rubric["allowed_fields"]},
            required_fields=tuple(rubric["required_fields"]),
            excluded_reference=fields["ticket_reference"],
        )
        review = reviewed_label(run, annotations, case)
        reply, complete = model_reply(run, case)
        label = ReplyReview(**review["annotation"]) if review and complete else None
        results[case] = evaluate_reply(expectation, reply, label)

    risks = {}
    for test, risk in (("T01", "B-04"), ("T02", "B-05")):
        verdicts = [result for case, result in results.items() if case.startswith(test)]
        risks[risk] = "FAIL" if "FAIL" in verdicts else "PASS" if all(v == "PASS" for v in verdicts) else "INCONCLUSIVE"
    print(json.dumps({
        "run_id": run_record["run_id"], "variants": results, "standalone_model": risks,
        "open_webui_integration": {"REQ-07": "NOT_TESTED", "REQ-08": "NOT_TESTED"},
    }, indent=2))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="operation", required=True)
    start = commands.add_parser("start")
    start.add_argument("artifact_dir", type=Path)
    commands.add_parser("preflight")
    run = commands.add_parser("capture")
    run.add_argument("run_dir", type=Path)
    for operation in ("follow-up", "score"):
        review_command = commands.add_parser(operation)
        review_command.add_argument("run_dir", type=Path)
        review_command.add_argument("review_json", type=Path)
    args = parser.parse_args()
    if args.operation == "start":
        start_lab(args.artifact_dir)
    elif args.operation == "preflight":
        print(json.dumps(verify_runtime(), indent=2, ensure_ascii=False))
    elif args.operation == "capture":
        run_initial(args.run_dir)
    else:
        action = follow_up if args.operation == "follow-up" else score
        action(args.run_dir, read_json(args.review_json))


if __name__ == "__main__":
    main()
