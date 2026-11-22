"""Run the preregistered P-006 Phase A fixture calls and preserve raw events."""

import argparse
import hashlib
import json
import os
import platform
import subprocess
import sys
from pathlib import Path
from tempfile import TemporaryDirectory
from uuid import uuid4


HERE = Path(__file__).resolve().parent
SOURCE = HERE.parents[1] / "6.1.1"
PLAN_PATH = HERE / "plan.json"
PLAN = json.loads(PLAN_PATH.read_text(encoding="utf-8"))
sys.path[:0] = [str(SOURCE / "model-evaluation"), str(SOURCE / "practice-lab")]
import evaluate as single
import fetch_model

BASE_RUNTIME = single.PLAN


def checked_inputs():
    for relative, expected in PLAN["source_sha256"].items():
        if single.sha256_file(SOURCE / relative) != expected:
            raise ValueError(f"Frozen 6.1.1 source hash mismatch: {relative}")
    return single.checked_fixtures()


def sha256_text(value):
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def scheduled(model, variants):
    for mode in PLAN["mode_order"]:
        for seed in PLAN["modes"][mode]["seeds"]:
            for case in variants:
                yield {"model": model, "mode": mode, "seed": seed, "case": case}


def call_key(case):
    return ":".join(str(case[field]) for field in ("model", "mode", "seed", "case"))


def generation(case):
    mode = PLAN["modes"][case["mode"]]
    return {**PLAN["shared_generation"], **mode["decoding"], "seed": case["seed"]}


def initialize(directory):
    directory.mkdir(mode=0o700)
    single.write_json(directory / "run.json", {
        "run_id": str(uuid4()),
        "created_at": single.utc_now(),
        "base_commit": PLAN["base_commit"],
        "runner_commit": subprocess.check_output(
            ["git", "-C", str(HERE), "rev-parse", "HEAD"], text=True
        ).strip(),
        "plan_sha256": single.sha256_file(PLAN_PATH),
        "code_sha256": {
            name: single.sha256_file(HERE / name)
            for name in ("study.py", "adjudicate.py")
        },
        "python": platform.python_version(),
        "machine": platform.machine(),
    })


def checked_run(directory):
    run = single.read_json(directory / "run.json")
    if run["plan_sha256"] != single.sha256_file(PLAN_PATH):
        raise ValueError("Capture plan differs from run initialization")
    for name, sha in run["code_sha256"].items():
        if single.sha256_file(HERE / name) != sha:
            raise ValueError(f"Phase A code differs from run initialization: {name}")
    return run


def artifact(model, directory):
    # The existing downloader accepts a plan file. Keep this adaptation outside 6.1.1.
    with TemporaryDirectory(prefix="p006-artifact-plan-") as work:
        local_plan = Path(work) / "plan.json"
        single.write_json(local_plan, {"model": PLAN["models"][model]})
        fetch_model.PLAN_PATH = local_plan
        fetch_model.download(directory)


def configure_runtime(model, run):
    engine = PLAN["engine"]
    spec = PLAN["models"][model]
    name = f"p006-phase-a-{run['run_id'][:8]}-{model.replace('.', '-')}"
    single.PLAN = {
        **BASE_RUNTIME,
        "model": spec,
        "container": name,
        "image": engine["image"],
        "engine_build": engine["build"],
        "platform": engine["platform"],
        "route": engine["route"],
        "server_args": [
            "--model", single.MODEL_IN_CONTAINER, "--alias", spec["alias"],
            "--host", "127.0.0.1", "--port", "8080", "--ctx-size", str(engine["context"]),
            "--threads", str(engine["threads"]), "--n-gpu-layers", "0",
            "--parallel", "1", "--no-webui", "--jinja", "--no-warmup",
        ],
    }
    return name


def append(handle, run, event, **fields):
    handle.write(json.dumps({
        "event": event, "run_id": run["run_id"], "recorded_at": single.utc_now(), **fields
    }, ensure_ascii=False) + "\n")
    handle.flush()
    os.fsync(handle.fileno())


def http(endpoint, body):
    try:
        return single.request(endpoint, body)
    except subprocess.TimeoutExpired as error:
        return {
            "endpoint": endpoint,
            "error": "transport timeout",
            "finished_at": single.utc_now(),
            "partial_stdout": (error.stdout or b"").decode("utf-8", errors="replace"),
            "partial_stderr": (error.stderr or b"").decode("utf-8", errors="replace"),
        }


def capture(handle, run, case, messages, parent_id=None):
    request = {
        "model": PLAN["models"][case["model"]]["alias"],
        "messages": messages,
        **generation(case),
    }
    body = json.dumps(request, ensure_ascii=False, separators=(",", ":")) + "\n"
    attempt_id = str(uuid4())
    append(handle, run, "request", case=case, attempt_id=attempt_id, parent_attempt_id=parent_id,
           body=body, body_sha256=sha256_text(body))
    # The template route renders the same request without generating tokens.
    template = http("/apply-template", body)
    append(handle, run, "template", attempt_id=attempt_id, record=template)
    completion = http("/v1/chat/completions", body)
    append(handle, run, "completion", attempt_id=attempt_id, record=completion)
    print(f"{call_key(case)} {attempt_id} HTTP {completion.get('http_status')}", flush=True)


def run_batch(directory, model, stage, model_dir, work, decisions=()):
    run = checked_run(directory)
    with (directory / f"{model}-{stage}.jsonl").open("x", encoding="utf-8") as ledger:
        for case, status, reason in decisions:
            append(ledger, run, "disposition", case=case, status=status, reason=reason)
        if not work:
            return
        name = configure_runtime(model, run)
        existing = single.docker("container", "inspect", name)
        if existing.returncode == 0:
            raise ValueError(f"Container name already exists: {name}")
        try:
            single.start_lab(model_dir)
            observed = single.verify_runtime()
        except (OSError, ValueError, RuntimeError, subprocess.SubprocessError) as error:
            for case, _, _ in work:
                append(ledger, run, "disposition", case=case, status="BLOCKED", reason=str(error))
            print(f"{model} {stage} blocked at runtime preflight: {error}", flush=True)
        else:
            append(ledger, run, "runtime", model=model, stage=stage, observed=observed)
            for case, messages, parent_id in work:
                capture(ledger, run, case, messages, parent_id)
        finally:
            container = single.docker("container", "inspect", name)
            if container.returncode == 0:
                state = json.loads(container.stdout)[0]
                if state["Config"]["Labels"].get("caseb.lab") == PLAN["lab"]:
                    stopped = single.docker("stop", "--timeout", "5", state["Id"])
                    removed = single.docker("rm", state["Id"])
                    append(ledger, run, "teardown", model=model, stage=stage,
                           stop_exit=stopped.returncode, remove_exit=removed.returncode)
            single.PLAN = BASE_RUNTIME


def fresh(directory, model, model_dir, fixtures):
    work = [
        (case, [single.first_message(fixtures, case["case"])], None)
        for case in scheduled(model, PLAN["fresh_cases"])
    ]
    run_batch(directory, model, "fresh", model_dir, work)


def records(directory):
    run = checked_run(directory)
    attempts, dispositions = {}, {}
    seen_cases = set()
    for model in PLAN["model_order"]:
        for stage in ("fresh", "follow-up"):
            path = directory / f"{model}-{stage}.jsonl"
            if not path.exists():
                continue
            runtime = None
            for line in path.read_text(encoding="utf-8").splitlines():
                event = json.loads(line)
                if event["run_id"] != run["run_id"]:
                    raise ValueError(f"Mixed run IDs in {path}")
                kind = event["event"]
                if kind == "runtime":
                    runtime = event["observed"]
                elif kind in ("request", "disposition"):
                    key = call_key(event["case"])
                    if key in seen_cases or event["case"]["model"] != model:
                        raise ValueError(f"Repeated or misfiled case: {key}")
                    seen_cases.add(key)
                    if kind == "request":
                        if runtime is None or sha256_text(event["body"]) != event["body_sha256"]:
                            raise ValueError(f"No verified runtime or request hash mismatch for {key}")
                        if event["attempt_id"] in attempts:
                            raise ValueError("Duplicate attempt ID")
                        attempts[event["attempt_id"]] = {"request": event, "runtime": runtime}
                    else:
                        dispositions[key] = event
                elif kind in ("template", "completion"):
                    attempt = attempts[event["attempt_id"]]
                    if kind in attempt:
                        raise ValueError("Duplicate model observation")
                    attempt[kind] = event["record"]
    return attempts, dispositions


def make_parser():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="operation", required=True)
    init = commands.add_parser("init")
    init.add_argument("run", type=Path)
    fetch = commands.add_parser("fetch")
    fetch.add_argument("model", choices=PLAN["model_order"])
    fetch.add_argument("artifact_dir", type=Path)
    for name in ("fresh", "follow-up"):
        stage = commands.add_parser(name)
        stage.add_argument("run", type=Path)
        stage.add_argument("model", choices=PLAN["model_order"])
        stage.add_argument("artifact_dir", type=Path)
        if name == "follow-up":
            stage.add_argument("review", type=Path)
    return parser


def main():
    args = make_parser().parse_args()
    fixtures = checked_inputs()
    if args.operation == "init":
        initialize(args.run)
    elif args.operation == "fetch":
        artifact(args.model, args.artifact_dir)
    elif args.operation == "fresh":
        fresh(args.run, args.model, args.artifact_dir, fixtures)
    else:
        from adjudicate import follow_up

        follow_up(args.run, args.model, args.artifact_dir, args.review, fixtures)


if __name__ == "__main__":
    main()
