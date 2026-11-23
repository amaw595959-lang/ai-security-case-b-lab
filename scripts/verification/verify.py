#!/usr/bin/env python3
"""Run the offline engineering assurance suite and write a bounded JSON summary."""

import argparse
import importlib.util
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

from archives import (
    MODEL, PRACTICE, check_event_retest, check_preview_archive, check_sanitization,
    verify_manifests, verify_practice_transcript,
)
from catalog import check_catalog
from repository import COMPARISON, DEMO, EVENTS, Repository, git


ROOT = Path(__file__).resolve().parents[2]


class Report:
    def __init__(self):
        self.checks = []

    def add(self, name, status, *, observations=None, issues=None, exit_code=None):
        check = {"name": name, "status": status}
        if observations is not None:
            check["observations"] = observations
        if issues:
            check["issues"] = issues
        if exit_code is not None:
            check["exit_code"] = exit_code
        self.checks.append(check)
        print(f"{status:12} {name}")
        for issue in issues or []:
            print(f"  {issue}")
        return check

    def observed(self, name, check, repo):
        try:
            value = check(repo)
        except (OSError, ValueError, KeyError, IndexError, AttributeError, TypeError) as error:
            # Replays may process rejected data. Do not include its exception text.
            return self.add(name, "FAIL", issues=[f"Required evidence or schema check failed ({type(error).__name__})"])
        observations, issues = value if isinstance(value, tuple) else (value, [])
        return self.add(name, "FAIL" if issues else "PASS", observations=observations, issues=issues)

    def command(self, name, args, cwd, assess=None):
        # Capture output privately. Only recognized, bounded summaries are printed.
        environment = os.environ.copy()
        for variable in ("PYTHONOPTIMIZE", "GITHUB_TOKEN", "GH_TOKEN", "PYTEST_ADDOPTS"):
            environment.pop(variable, None)
        environment["PYTEST_DISABLE_PLUGIN_AUTOLOAD"] = "1"
        try:
            result = subprocess.run(args, cwd=cwd, env=environment, stdout=subprocess.PIPE,
                                    stderr=subprocess.STDOUT, check=False, encoding="utf-8", errors="replace", timeout=180)
        except FileNotFoundError:
            return self.add(name, "BLOCKED", issues=["Required executable is unavailable"])
        except subprocess.TimeoutExpired:
            return self.add(name, "BLOCKED", issues=["Execution exceeded its local time budget"])
        if result.returncode != 0:
            return self.add(name, "FAIL", exit_code=result.returncode,
                            issues=["Command failed. Run it locally for full diagnostic output."])
        try:
            details = assess(result.stdout) if assess else {}
        except (OSError, ValueError, KeyError):
            return self.add(name, "FAIL", exit_code=result.returncode,
                            issues=["Expected observations were missing or did not match the archive"])
        return self.add(name, "PASS", observations=details, exit_code=result.returncode)

    def result(self):
        statuses = {check["status"] for check in self.checks}
        if "FAIL" in statuses:
            return "FAIL", 1
        if "BLOCKED" in statuses:
            return "BLOCKED", 2
        return "PASS", 0


def count_result(pattern, key):
    def parse(text):
        match = re.search(pattern, text)
        if not match or int(match[1]) < 1:
            raise ValueError("Missing executed check count")
        return {key: int(match[1])}

    return parse


def standalone_result(repo):
    def compare(stdout):
        current = json.loads(stdout)
        archived = json.loads(repo.text(f"{MODEL}/evidence/results.json"))
        if current != archived:
            raise ValueError("Standalone replay differs")
        return {"variants": len(current["variants"]), "recorded_model_verdicts": current["standalone_model"]}

    return compare


def phase_a_result(stdout):
    match = re.search(r"Verified (\d+) request records, (\d+) complete replies, (\d+) dispositions", stdout)
    if not match:
        raise ValueError("Missing Phase A replay observations")
    return dict(zip(("requests", "complete_replies", "dispositions"), map(int, match.groups())))


def python_sources(repo):
    count, errors = 0, []
    for name in sorted(repo.names):
        if not name.endswith(".py"):
            continue
        try:
            compile(repo.path(name).read_bytes(), name, "exec", dont_inherit=True)
            count += 1
        except (OSError, ValueError, SyntaxError) as error:
            errors.append(f"{name}: Python compilation failed ({type(error).__name__})")
    return {"compiled_files": count}, errors


def references(report, repo, upstream):
    if importlib.util.find_spec("markdown_it") is None:
        report.add("Markdown and source references", "BLOCKED", issues=["Pinned Markdown parser is unavailable"])
        return
    from references import check_links, check_upstream, source_lock

    try:
        lock = source_lock(repo)
        counts, errors, missing = check_links(repo, lock)
    except (KeyError, OSError, TypeError, ValueError):
        report.add("Markdown and source references", "FAIL", issues=["Invalid source lock or unreadable Markdown"])
        return
    report.add("Markdown and source references", "FAIL" if errors else "BLOCKED" if missing else "PASS",
               observations=counts, issues=errors + [f"Pinned repository commit unavailable: {rev}" for rev in missing])
    if upstream is None:
        report.add("Open WebUI Git blob recheck", "NOT_TESTED",
                   issues=["No local upstream checkout supplied. The fast check used the pinned source lock."])
    else:
        try:
            issues = check_upstream(upstream, lock)
        except (OSError, subprocess.CalledProcessError):
            report.add("Open WebUI Git blob recheck", "BLOCKED", issues=["Upstream Git checkout is unavailable"])
        else:
            report.add("Open WebUI Git blob recheck", "FAIL" if issues else "PASS",
                       observations={"blobs": len(lock["files"]), "revision": lock["revision"]}, issues=issues)


def workflow_checks(report, repo, lint):
    if importlib.util.find_spec("yaml") is None:
        report.add("Workflow policy", "BLOCKED", issues=["Pinned YAML parser is unavailable"])
    else:
        from workflows import check_configuration

        report.observed("Workflow policy", check_configuration, repo)
    if lint:
        report.command("GitHub Actions syntax and expressions",
                       [lint, "-shellcheck=", "-pyflakes="], repo.root)
    else:
        report.add("GitHub Actions syntax and expressions", "BLOCKED", issues=["Pinned actionlint is unavailable"])


def run_suite(report, repo, upstream, lint):
    py = [sys.executable, "-B"]
    references(report, repo, upstream)
    report.observed("Canonical IDs and traces", check_catalog, repo)
    report.observed("Archived SHA-256 manifests", verify_manifests, repo)
    report.observed("Practice transcript checksums", verify_practice_transcript, repo)
    report.observed("Evidence sanitization and secret patterns", check_sanitization, repo)
    report.observed("Python compilation", python_sources, repo)
    names = sorted(name for name in repo.names if name.endswith(".py"))
    if importlib.util.find_spec("ruff") is None:
        report.add("Python static correctness", "BLOCKED", issues=["Pinned Ruff is unavailable"])
    else:
        report.command("Python static correctness", [*py, "-m", "ruff", "check", "--no-cache",
                       "--select", "E9,F63,F7,F82", "--", *names], repo.root)
    for name in sorted(name for name in repo.names if name.endswith(".sh")):
        report.command(f"Shell syntax {name}", ["bash", "-n", "--", name], repo.root)
    workflow_checks(report, repo, lint)
    if importlib.util.find_spec("pytest") is None:
        report.add("Case B practice suite", "BLOCKED", issues=["Pinned pytest is unavailable"])
    else:
        report.command("Case B practice suite", [*py, "-m", "pytest", "-p", "no:cacheprovider", "-q"],
                       repo.root / PRACTICE, count_result(r"(\d+) passed", "tests"))
    for check, directory in (("REQ-07 standalone HTTP/SQLite", DEMO), ("REQ-08 event policy", EVENTS),
                              ("Verification toolkit tests", "scripts/verification")):
        report.command(check, [*py, "-m", "unittest", "discover", "-s", "tests", "-v"],
                       repo.root / directory, count_result(r"Ran (\d+) tests?", "tests"))
    report.command("Standalone model evidence replay",
                   [*py, f"{MODEL}/evaluate.py", "score", f"{MODEL}/evidence/run", f"{MODEL}/evidence/review.json"],
                   repo.root, standalone_result(repo))
    report.command("Phase A evidence replay", [*py, f"{COMPARISON}/verify.py", f"{COMPARISON}/evidence/run"],
                   repo.root, phase_a_result)
    report.observed("REQ-07 archived preview and SQLite replay", check_preview_archive, repo)
    report.command("Phase C original evidence replay", [*py, f"{EVENTS}/verify.py"], repo.root)
    report.observed("Phase C scoped event and expiry replay", check_event_retest, repo)
    report.add("Fresh Docker and model integration", "NOT_TESTED",
               issues=["Outside the offline suite. See the guarded manual integration workflow."])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", dest="output", type=Path, required=True, help="write the bounded summary to this path")
    parser.add_argument("--upstream", type=Path, help="recheck the source lock against a local pinned Open WebUI checkout")
    parser.add_argument("--actionlint", default=shutil.which("actionlint"), help="path to the pinned actionlint executable")
    args = parser.parse_args()
    report = Report()
    revision = None
    try:
        repo = Repository(ROOT)
        revision = git(ROOT, "rev-parse", "HEAD").decode().strip()
    except (OSError, subprocess.CalledProcessError):
        report.add("Repository inventory", "BLOCKED", issues=["A readable Git working tree is required"])
    else:
        run_suite(report, repo, args.upstream, args.actionlint)
    status, code = report.result()
    run_id = os.environ.get("GITHUB_RUN_ID", "")
    summary = {
        "schema_version": 1, "scope": "offline", "revision": revision,
        "python": sys.version.split()[0], "github_run_id": run_id if run_id.isdecimal() else None,
        "status": status, "exit_code": code, "checks": report.checks,
    }
    args.output.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"{status} offline verification. Exit code {code}.")
    return code


if __name__ == "__main__":
    raise SystemExit(main())
