"""Check request and reply ancestry without running Docker or a model."""

import argparse
import json
from datetime import datetime
from pathlib import Path

import adjudicate
import study


def verify(directory):
    fixtures = study.checked_inputs()
    attempts, dispositions = study.records(directory)
    planned = {
        study.call_key(case)
        for model in study.PLAN["model_order"]
        for case in study.scheduled(model, (*study.PLAN["fresh_cases"], study.PLAN["conditional_case"]))
    }
    actual = {study.call_key(attempt["request"]["case"]) for attempt in attempts.values()}
    if actual | set(dispositions) != planned:
        raise ValueError("An attempted or explicitly unattempted planned case is missing")
    ids = set()
    complete_attempts = 0
    for attempt in attempts.values():
        request = attempt["request"]
        case = request["case"]
        runtime = attempt["runtime"]
        model = study.PLAN["models"][case["model"]]
        if (
            runtime["weights_sha256"] != model["weights_sha256"]
            or runtime["image"] != study.PLAN["engine"]["image"]
            or runtime["route"] != study.PLAN["engine"]["route"]
            or runtime["isolation"]["network_mode"] != "none"
            or runtime["isolation"]["port_bindings"]
        ):
            raise ValueError("Runtime differs from the isolated pinned target")
        if case["case"] == study.PLAN["conditional_case"]:
            parent = attempts[request["parent_attempt_id"]]
            prior = parent["request"]
            if prior["case"] != {**case, "case": "T01-A"}:
                raise ValueError("Follow-up crosses seed, model or conversation")
            messages = [
                *json.loads(prior["body"])["messages"],
                {"role": "assistant", "content": adjudicate.completed_reply(parent)},
                {"role": "user", "content": study.single.variant_inputs(fixtures, "T01-C")["request"]},
            ]
        else:
            if request["parent_attempt_id"] is not None:
                raise ValueError("Fresh case has previous conversation state")
            messages = [study.single.first_message(fixtures, case["case"])]
        expected = {"model": model["alias"], "messages": messages, **study.generation(case)}
        if json.loads(request["body"]) != expected:
            raise ValueError("Exact request differs from the frozen fixture and plan")

        if adjudicate.completed_reply(attempt) is not None:
            complete_attempts += 1
            payload = json.loads(attempt["completion"]["body"])
            started = datetime.fromisoformat(attempt["completion"]["started_at"])
            finished = datetime.fromisoformat(attempt["completion"]["finished_at"])
            requested = datetime.fromisoformat(request["recorded_at"])
            if not requested <= started <= finished or payload["id"] in ids:
                raise ValueError("Unexpected chronology or repeated completion ID")
            if payload["usage"]["prompt_tokens_details"]["cached_tokens"] != 0:
                raise ValueError("Provider reported reused prompt tokens")
            ids.add(payload["id"])
    print(f"Verified {len(attempts)} request records, {complete_attempts} complete replies, "
          f"{len(dispositions)} dispositions and the frozen schedule.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("run", type=Path)
    verify(parser.parse_args().run)
