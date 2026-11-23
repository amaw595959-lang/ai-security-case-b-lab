"""Constrain workflow permissions, triggers and reviewed action pins."""

from yaml import YAMLError, safe_load


ACTIONS = {
    "actions/checkout": "11bd71901bbe5b1630ceea73d27597364c9af683",
    "actions/setup-python": "a26af69be951a213d495a4c3e4e4022e16d87065",
    "actions/upload-artifact": "ea165f8d65b6e75b540449e92b4886f43607fa02",
}
FAST = ".github/workflows/verify.yml"
MANUAL = ".github/workflows/integration.yml"
GUARD = "${{ github.ref == 'refs/heads/main' && inputs.confirm_isolated }}"
READ_ONLY = {"contents": "read"}


def check_configuration(repo):
    names = {name for name in repo.names if name.startswith(".github/workflows/") and name.endswith((".yml", ".yaml"))}
    errors = []
    if {FAST, MANUAL} - names:
        errors.append("Required fast and manual workflow files are missing")
    action_count = 0
    for name in sorted(names):
        try:
            workflow = safe_load(repo.text(name))
            triggers = set(workflow["on"])
            jobs = workflow["jobs"]
            if not isinstance(jobs, dict) or not jobs:
                raise ValueError("Missing jobs")
        except (OSError, ValueError, YAMLError, TypeError, KeyError):
            errors.append(f"{name}: unreadable workflow or invalid structure")
            continue
        if workflow.get("permissions") != READ_ONLY:
            errors.append(f"{name}: expected contents: read workflow permissions")
        allowed = {"workflow_dispatch"} if name == MANUAL else {"pull_request", "push", "workflow_dispatch"}
        if not triggers or triggers - allowed or (name == FAST and "pull_request" not in triggers):
            errors.append(f"{name}: unapproved workflow trigger set")
        for label, job in jobs.items():
            if not isinstance(job, dict):
                errors.append(f"{name}: malformed job")
                continue
            if job.get("permissions", READ_ONLY) != READ_ONLY:
                errors.append(f"{name}: job overrides the read-only permission")
            if job.get("runs-on") != "ubuntu-24.04":
                errors.append(f"{name}: expected an ephemeral Ubuntu GitHub-hosted runner")
            if name == MANUAL and job.get("if") != GUARD:
                errors.append(f"{name}: manual job lacks its protected main and explicit isolation guards")
            for step in job.get("steps", []):
                if not isinstance(step, dict):
                    errors.append(f"{name}: malformed step")
                    continue
                if "secrets." in str(step) or "secrets[" in str(step):
                    errors.append(f"{name}: steps must have no secret inputs")
                if uses := step.get("uses"):
                    action_count += 1
                    action, _, pin = uses.partition("@")
                    if ACTIONS.get(action) != pin:
                        errors.append(f"{name}: action reference is outside the reviewed pin list")
                    if action == "actions/checkout" and step.get("with", {}).get("persist-credentials") is not False:
                        errors.append(f"{name}: checkout credentials would persist")
    return {"workflows": len(names), "pinned_steps": action_count}, errors
