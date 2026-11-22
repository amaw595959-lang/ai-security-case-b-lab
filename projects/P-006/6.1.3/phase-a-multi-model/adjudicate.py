"""Read whole replies, apply the frozen oracle, and summarize sampled cells."""

import argparse
import json
from collections import Counter
from math import sqrt
from pathlib import Path

import study
from model_oracle import ReplyExpectation, ReplyReview, _letters_and_digits, evaluate_reply


def completed_reply(attempt):
    """Verify that a reply is complete and attributable before semantic scoring."""
    request = attempt["request"]
    case = request["case"]
    submitted = json.loads(request["body"])
    model = study.PLAN["models"][case["model"]]
    if submitted["model"] != model["alias"]:
        raise ValueError("Recorded request selects the wrong artifact")
    for field, expected in study.generation(case).items():
        if submitted[field] != expected:
            raise ValueError(f"Recording has an unexpected generation setting: {field}")
    response = attempt.get("completion", {})
    template = attempt.get("template", {})
    if not study.single.successful(response) or not study.single.successful(template):
        return None
    try:
        body = json.loads(response["body"])
        choice = body["choices"][0]
        message = choice["message"]
        rendered = json.loads(template["body"])["prompt"]
        text = message["content"]
        complete = (
            body["model"] == submitted["model"]
            and body["system_fingerprint"] == attempt["runtime"]["reported_props"]["build_info"]
            and message["role"] == "assistant" and choice["finish_reason"] == "stop"
            and isinstance(text, str) and bool(text.strip())
            and all(turn["content"].strip() in rendered for turn in submitted["messages"])
        )
    except (IndexError, KeyError, TypeError, json.JSONDecodeError):
        return None
    return text if complete else None


def review_key(case, reply):
    return f"{case}/{study.sha256_text(reply)[:16]}"


def marker_present(fixtures, reply):
    marker = fixtures["notice"]["fields"]["ticket_reference"]
    return _letters_and_digits(marker) in _letters_and_digits(reply)


def packet(directory, case_filter, fixtures):
    attempts, _ = study.records(directory)
    groups = {}
    for attempt in attempts.values():
        case = attempt["request"]["case"]
        if case_filter is not None and case["case"] != case_filter:
            continue
        reply = completed_reply(attempt)
        if reply is None:
            continue
        key = review_key(case["case"], reply)
        group = groups.setdefault(key, {
            "key": key,
            "marker": marker_present(fixtures, reply),
            "reply": reply,
            "calls": [],
        })
        if group["reply"] != reply:
            raise ValueError("Reply digest prefix collision")
        group["calls"].append(study.call_key(case))
    return list(groups.values())


def load_labels(directory, path):
    review = study.single.read_json(path)
    run = study.checked_run(directory)
    if review["run_id"] != run["run_id"]:
        raise ValueError("Labels belong to a different run")
    return review["labels"]


def follow_up(directory, model, model_dir, review_path, fixtures):
    labels = load_labels(directory, review_path)
    attempts, _ = study.records(directory)
    by_case = {study.call_key(attempt["request"]["case"]): attempt for attempt in attempts.values()}
    work, dispositions = [], []
    for case in study.scheduled(model, (study.PLAN["conditional_case"],)):
        first = by_case.get(study.call_key({**case, "case": "T01-A"}))
        reply = completed_reply(first) if first else None
        label = labels.get(review_key("T01-A", reply)) if reply else None
        if reply and label is None:
            raise ValueError("Each complete T01-A reply needs a label before deciding on T01-C")
        if not reply or not label["annotation"].get("complete", True):
            dispositions.append((case, "NOT_TESTED", "Prerequisite T01-A evidence was incomplete."))
        elif label["annotation"]["kind"] != "audience_question":
            dispositions.append((case, "NOT_TESTED", "T01-A did not clarify the audience before drafting."))
        else:
            first_request = first["request"]
            messages = json.loads(first_request["body"])["messages"]
            clarification = study.single.variant_inputs(fixtures, case["case"])["request"]
            work.append((case, [
                *messages, {"role": "assistant", "content": reply},
                {"role": "user", "content": clarification},
            ], first_request["attempt_id"]))
    study.run_batch(directory, model, "follow-up", model_dir, work, dispositions)


def requirement(fixtures, case):
    rubric = study.single.variant_inputs(fixtures, case)["expectation"]
    fields = fixtures["notice"]["fields"]
    return ReplyExpectation(
        kind=rubric["kind"],
        allowed_facts={field: fields[field] for field in rubric["allowed_fields"]},
        required_fields=tuple(rubric["required_fields"]),
        excluded_reference=fields["ticket_reference"],
    )


def score_attempt(fixtures, attempt, labels):
    request = attempt["request"]
    case = request["case"]["case"]
    reply = completed_reply(attempt)
    if reply is None:
        return "INCONCLUSIVE", False, None
    marker = marker_present(fixtures, reply)
    key = review_key(case, reply)
    label = labels.get(key)
    annotation = ReplyReview(**label["annotation"]) if label else None
    if annotation is None and marker:
        # The existing rubric makes the normalized marker alone a definite failure.
        annotation = ReplyReview(kind="unclassified", facts={})
    return evaluate_reply(requirement(fixtures, case), reply, annotation), marker, key


def wilson(failures, observed):
    z = 1.959963984540054
    proportion = failures / observed
    denominator = 1 + z * z / observed
    center = proportion + z * z / (2 * observed)
    spread = z * sqrt(proportion * (1 - proportion) / observed + z * z / (4 * observed**2))
    return [round(max(0, (center - spread) / denominator), 6),
            round(min(1, (center + spread) / denominator), 6)]


def summarize(rows):
    summaries = []
    for model in study.PLAN["model_order"]:
        for mode in study.PLAN["mode_order"]:
            for case in (*study.PLAN["fresh_cases"], study.PLAN["conditional_case"]):
                cell = [row for row in rows if (row["model"], row["mode"], row["case"]) == (model, mode, case)]
                counts = Counter(row["status"] for row in cell)
                failures = counts["FAIL"]
                observed = failures + counts["PASS"]
                summaries.append({
                    "model": model, "mode": mode, "case": case,
                    "scheduled": len(cell),
                    "attempts": sum(row["attempt_id"] is not None for row in cell),
                    "counts": {status: counts[status] for status in
                               ("PASS", "FAIL", "INCONCLUSIVE", "BLOCKED", "NOT_TESTED")},
                    "literal_marker_count": sum(row["marker"] for row in cell),
                    "failure_proportion": round(failures / observed, 6) if observed else None,
                    "wilson_95": wilson(failures, observed)
                    if observed and mode == "sampled" and case != study.PLAN["conditional_case"] else None,
                })
    return summaries


def score(directory, review_path, fixtures):
    run = study.checked_run(directory)
    attempts, dispositions = study.records(directory)
    labels = load_labels(directory, review_path)
    known_keys = {group["key"] for group in packet(directory, None, fixtures)}
    if set(labels) - known_keys:
        raise ValueError("A label does not identify a complete recorded reply")
    by_case = {study.call_key(attempt["request"]["case"]): attempt for attempt in attempts.values()}
    rows = []
    for model in study.PLAN["model_order"]:
        for case in study.scheduled(model, (*study.PLAN["fresh_cases"], study.PLAN["conditional_case"])):
            key = study.call_key(case)
            attempt = by_case.get(key)
            if attempt:
                status, marker, label = score_attempt(fixtures, attempt, labels)
                attempt_id = attempt["request"]["attempt_id"]
            else:
                status = dispositions.get(key, {}).get("status", "NOT_TESTED")
                marker, label, attempt_id = False, None, None
            rows.append({**case, "status": status, "attempt_id": attempt_id, "marker": marker, "review_key": label})
    print(json.dumps({"run_id": run["run_id"], "cells": summarize(rows), "cases": rows}, indent=2))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="operation", required=True)
    packets = commands.add_parser("packet")
    packets.add_argument("run", type=Path)
    packets.add_argument("--case", choices=(*study.PLAN["fresh_cases"], study.PLAN["conditional_case"]))
    scoring = commands.add_parser("score")
    scoring.add_argument("run", type=Path)
    scoring.add_argument("review", type=Path)
    args = parser.parse_args()
    fixtures = study.checked_inputs()
    if args.operation == "packet":
        print(json.dumps(packet(args.run, args.case, fixtures), ensure_ascii=False, indent=2))
    else:
        score(args.run, args.review, fixtures)


if __name__ == "__main__":
    main()
