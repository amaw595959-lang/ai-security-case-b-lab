"""Check canonical identifiers and their documented, bidirectional trace."""

import re

from repository import DESIGN, P006, sha256


RISK_FILE = "strategy/110-risks.md"
WORK_FILE = "strategy/334-subsublayers.md"
PROJECT_FILE = "strategy/116-projects.md"
WORK_ID_DIGEST = "5deb27c80f75c91e178790329a298bba83793cd8b1a2611f04cb1ed31755ed33"


def numbered(prefix, stop):
    return {f"{prefix}{number:02}" for number in range(1, stop + 1)}


def compact_ids(text, prefix):
    pattern = rf"\b{re.escape(prefix)}(\d+(?:/\d+)*)\b"
    return {prefix + item for result in re.findall(pattern, text) for item in result.split("/")}


def unique_keys(items, required):
    return set(items) == required and len(items) == len(required)


def table(text, key_pattern, errors):
    rows = {}
    for line in text.splitlines():
        if not line.startswith("| ") or not line.endswith(" |"):
            continue
        key, *cells = line[2:-2].split(" | ")
        match = re.fullmatch(key_pattern, key)
        if not match:
            continue
        identifier = match[1]
        if identifier in rows:
            errors.append(f"Traceability repeats {identifier}")
        rows[identifier] = cells
    return rows


def check_catalog(repo):
    errors = []
    risks = numbered("B-", 73) | numbered("R-", 37)
    declared_risks = re.findall(r"^\d+\. \*\*([BR]-\d+) — ", repo.text(RISK_FILE), re.M)
    if not unique_keys(declared_risks, risks):
        errors.append("The 110 canonical B/R risk declarations differ from the required set")
    work_source = repo.text(WORK_FILE)
    work = re.findall(r"^- \[[ xX]\] \*\*(\d+\.\d+\.\d+)\*\* — (.+)$", work_source, re.M)
    work_ids = [name for name, _ in work]
    anchored = sha256(("\n".join(sorted(work_ids)) + "\n").encode())
    if len(work_ids) != 334 or len(set(work_ids)) != 334 or anchored != WORK_ID_DIGEST:
        errors.append("The 334 canonical work package IDs differ from the pinned inventory")
    expected_project = "Secure-by-Default LLM Application Reference Architecture"
    projects = re.findall(r"^- \*\*P-006\*\* — (.+)$", repo.text(PROJECT_FILE), re.M)
    if projects != [expected_project]:
        errors.append("P-006 project identity does not match the canonical title")
    for name in ("6.1.1", "6.1.2"):
        if "`P-006`" not in dict(work).get(name, ""):
            errors.append(f"{name} no longer maps to P-006")

    req = numbered("REQ-", 9)
    inv = numbered("INV-", 7)
    tests = numbered("T", 4)
    micro = numbered("6.1.1-MT", 14)
    requirements = repo.text(f"{DESIGN}/security-requirements.md")
    design = repo.text(f"{DESIGN}/case-b-test-design.md")
    bounds = repo.text(f"{DESIGN}/trust-boundaries.md")
    supplement = f"{DESIGN}/microtasks"
    trace = repo.text(f"{supplement}/requirements-traceability.md")
    if not unique_keys(re.findall(r"^### P006-611-(REQ-\d+) — ", requirements, re.M), req):
        errors.append("Nine requirements must be defined exactly once")
    canon_inv = table(requirements, r"`P006-611-(INV-\d+)`", errors)
    if set(canon_inv) != inv:
        errors.append("Seven invariants must be defined")
    expected_tests = {}
    for name, section in re.findall(r"^### P006-611-(T\d+) — [^\n]+\n([\s\S]*?)(?=^#{1,3} |\Z)", design, re.M):
        objective = re.search(r"^\*\*Objective and mapping\*\*.+$", section, re.M)
        if name in expected_tests:
            errors.append(f"Canonical test repeated {name}")
        expected_tests[name] = objective[0] if objective else ""
    if set(expected_tests) != tests or not all(expected_tests.values()):
        errors.append("Four canonical tests must have an objective and mapping")

    for filename in ("microtask-coverage.md", "review-and-acceptance.md"):
        section = repo.text(f"{supplement}/{filename}")
        rows = table(section, r"(6\.1\.1-MT\d+)", errors)
        if set(rows) != micro or not all(len(cells) >= 2 and all(cells) for cells in rows.values()):
            errors.append(f"{filename}: all 14 micro-tasks require a completed row")

    for name in sorted(repo.names):
        if not name.startswith(f"{P006}/") or not name.endswith(".md"):
            continue
        doc = repo.text(name)
        unknown = (set(re.findall(r"\b[BR]-\d+\b", doc)) - risks)
        for prefix, known in (("REQ-", req), ("INV-", inv), ("T", tests), ("6.1.1-MT", micro)):
            unknown |= compact_ids(doc, prefix) - known
        if unknown:
            errors.append(f"{name}: references identifiers absent from the canonical catalogs")

    forward = table(trace, r"\[P006-611-(REQ-\d+)\]\([^)]+\) · .+", errors)
    evidence = table(trace, r"(REQ-\d+)", errors)
    if set(forward) != req or set(evidence) != req:
        errors.append("Each requirement needs forward and evidence/ownership rows")
    for name, cells in evidence.items():
        if len(cells) != 3 or not all(cells) or "](" not in cells[0] or len(cells[2].split()) < 3:
            errors.append(f"{name}: evidence, residual risk or accountable role is incomplete")
    reverse_invariants = table(trace, r"P006-611-(INV-\d+)", errors)
    canonical = {name: compact_ids(fields[-1], "REQ-") for name, fields in canon_inv.items() if fields}
    reversed_inv = {name: compact_ids(fields[0], "REQ-") for name, fields in reverse_invariants.items() if fields}
    if canonical != reversed_inv:
        errors.append("Reverse invariant mapping disagrees with canonical requirements")
    for name, detail in forward.items():
        expected = {identifier for identifier, linked in canonical.items() if name in linked}
        if len(detail) != 4 or not all(detail) or compact_ids(detail[2], "INV-") != expected:
            errors.append(f"{name}: forward control or invariant mappings are incomplete")

    canonical_boundaries = {}
    for number, section in re.findall(r"^### ([1-8]) — [^\n]+\n([\s\S]*?)(?=^#{1,3} |\Z)", bounds, re.M):
        mapping = re.search(r"\*\*Maps to\*\* (.+)$", section, re.M)
        if mapping:
            canonical_boundaries[number] = mapping[1]
    boundary_rows = table(trace, r"([1-8]) · .+", errors)
    if set(canonical_boundaries) != set("12345678") or set(boundary_rows) != set(canonical_boundaries):
        errors.append("Eight trace boundaries must match the canonical architecture")
    for number, cells in boundary_rows.items():
        if number not in canonical_boundaries or not cells:
            continue
        for prefix in ("REQ-", "INV-"):
            if compact_ids(cells[0], prefix) != compact_ids(canonical_boundaries[number], prefix):
                errors.append(f"Boundary {number}: {prefix} mapping drifted")

    reverse_tests = table(trace, r"\[P006-611-(T\d+)\]\([^)]+\)", errors)
    if set(reverse_tests) != tests:
        errors.append("Each canonical test needs a reverse trace row")
    for name, cells in reverse_tests.items():
        for prefix in ("REQ-", "INV-"):
            expected = compact_ids(expected_tests.get(name, ""), prefix)
            if not cells or compact_ids(cells[0], prefix) != expected:
                errors.append(f"{name}: {prefix} mapping disagrees with the test objective")
        objective = expected_tests.get(name, "")
        direct = re.search(r"Direct requirement `P006-611-(REQ-\d+)`", objective)
        requirements_to_check = {direct[1]} if direct else compact_ids(objective, "REQ-")
        for name_req in requirements_to_check:
            row = evidence.get(name_req, [])
            if not row or f"P006-611-{name}" not in row[0]:
                errors.append(f"{name_req}: evidence row does not identify {name}")

    reverse_risks = table(trace, r"([BR]-\d+) — .+", errors)
    forward_risks = {}
    for name, cells in forward.items():
        if len(cells) < 3:
            continue
        for risk in re.findall(r"\b[BR]-\d+\b", cells[2]):
            forward_risks.setdefault(risk, set()).add(name)
    inverted = {name: compact_ids(fields[0], "REQ-") for name, fields in reverse_risks.items() if fields}
    if forward_risks != inverted or not {"B-04", "B-05"} <= set(inverted):
        errors.append("Risk mappings disagree between the forward and reverse traces")

    return {
        "risks": len(declared_risks), "work_packages": len(work_ids), "project": "P-006",
        "micro_tasks": len(micro), "requirements": len(evidence), "invariants": len(canon_inv),
        "boundaries": len(canonical_boundaries), "tests": len(expected_tests),
    }, errors
