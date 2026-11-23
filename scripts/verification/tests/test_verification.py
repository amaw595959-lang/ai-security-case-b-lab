import gzip
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from archives import check_event_retest, check_sanitization, json_rows, verify_manifests
from catalog import PROJECT_FILE, RISK_FILE, WORK_FILE, check_catalog
from references import check_links, headings
from repository import DESIGN, EVENTS, PIN, Repository, sha256
from verify import ROOT, Report
from workflows import ACTIONS, FAST, GUARD, MANUAL, check_configuration


LOCK = {"revision": PIN, "files": {}}


class RepositoryFixture(unittest.TestCase):
    def setUp(self):
        folder = tempfile.TemporaryDirectory()
        self.addCleanup(folder.cleanup)
        self.root = Path(folder.name)

    def put(self, name, content):
        path = self.root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        return path

    def repo(self):
        paths = [path.relative_to(self.root).as_posix() for path in self.root.rglob("*")
                 if path.is_file() or path.is_symlink()]
        return Repository(self.root, paths)


class ReferenceTests(RepositoryFixture):
    def test_local_reference_and_duplicate_heading(self):
        self.put("docs/Notes Here.md", '# **Audit**\n# Audit\n<a name="old-audit"></a>\n')
        self.put("README.md", """
| Reference |
| --- |
| [Revision][target] |

[target]: <docs/Notes Here.md#audit-1>

[Prior anchor](docs/Notes%20Here.md#old-audit)

~~~markdown
[Illustration](missing-example.md)
~~~
""")
        counts, errors, missing = check_links(self.repo(), LOCK)
        self.assertEqual((counts["local_links"], errors, missing), (2, [], []))

    def test_reports_missing_file_and_anchor(self):
        self.put("README.md", "# Known\n[bad](#unknown) [different case](readme.md)")
        _, errors, _ = check_links(self.repo(), LOCK)
        self.assertEqual(len(errors), 2)

    def test_pinned_source_range_rejects_missing_path_and_wrong_line(self):
        link = f"https://github.com/open-webui/open-webui/blob/{PIN}"
        self.put("README.md", f"[known]({link}/main.py#L3-L8) [absent]({link}/missing.py#L1)")
        lock = {"revision": PIN, "files": {"main.py": {"lines": 6}}}
        _, errors, _ = check_links(self.repo(), lock)
        self.assertEqual(len(errors), 2)
        self.assertEqual(headings("# File \u2014 `Line`"), {"file--line"})


class ManifestTests(RepositoryFixture):
    def test_valid_manifest_can_name_approved_parent_file(self):
        self.put("demo/replay.py", "example")
        name = "demo/evidence/SHA256SUMS"
        manifest = f"{sha256(b'example')}  ../replay.py\n"
        self.put(name, manifest)
        observed, errors = verify_manifests(self.repo(), {name: (1, sha256(manifest.encode()))})
        self.assertEqual(errors, [])
        self.assertEqual(observed[name]["verified"], 1)

    def test_changes_to_file_and_manifest_do_not_replace_accepted_evidence(self):
        self.put("evidence/claim.json", "{}")
        name = "evidence/SHA256SUMS"
        self.put(name, f"{sha256(b'{}')}  claim.json\n")
        observed, errors = verify_manifests(self.repo(), {name: (1, sha256(b"prior pinned bytes"))})
        self.assertEqual(observed[name]["verified"], 1)
        self.assertTrue(any("accepted manifest" in issue for issue in errors))

    def test_missing_evidence_and_missing_known_manifest_fail(self):
        self.put("evidence/SHA256SUMS", f"{'0' * 64}  deleted.json\n")
        _, errors = verify_manifests(self.repo(), {"baseline/SHA256SUMS": (1, "0" * 64)})
        self.assertEqual(len(errors), 2)

    def test_tampered_evidence_and_duplicate_target_fail(self):
        self.put("evidence/claim.json", "{}")
        line = f"{'0' * 64}  claim.json"
        self.put("evidence/SHA256SUMS", f"{line}\n{line}\n")
        _, errors = verify_manifests(self.repo(), {})
        self.assertTrue(any("mismatch" in issue for issue in errors))
        self.assertTrue(any("repeated target" in issue for issue in errors))

    def test_external_and_symlink_targets_are_rejected(self):
        (self.root / "evidence").mkdir()
        (self.root / "evidence/alias").symlink_to(self.root.parent / "outside")
        self.put("evidence/SHA256SUMS", f"{'0' * 64}  ../../outside\n{'0' * 64}  alias\n")
        _, errors = verify_manifests(self.repo(), {})
        self.assertEqual(len(errors), 2)
        self.assertTrue(all("unsafe" in issue for issue in errors))


class EvidenceSanitizationTests(RepositoryFixture):
    def test_rejects_unredacted_field_without_echoing_value(self):
        self.put("lab/evidence/example.json", json.dumps({"authorization": "private sample"}))
        _, errors = check_sanitization(self.repo())
        self.assertEqual(len(errors), 1)
        self.assertNotIn("private sample", errors[0])

    def test_checks_compressed_archive_and_reserved_fixture_identities(self):
        self.put("lab/evidence/public.json", json.dumps({
            "email": "reader@example.com", "api_keys": False, "password": "[redacted]",
        }))
        compressed = self.root / "lab/evidence/record.log.gz"
        token = "ghp_" + "x" * 36
        compressed.write_bytes(gzip.compress(token.encode()))
        _, errors = check_sanitization(self.repo())
        self.assertEqual(len(errors), 1)
        self.assertIn("possible GitHub token", errors[0])
        self.assertNotIn(token, errors[0])

    def test_unreadable_binary_evidence_is_not_a_pass(self):
        self.put("lab/evidence/record.bin", "").write_bytes(b"\xff")
        _, errors = check_sanitization(self.repo())
        self.assertTrue(any("cannot be scanned" in issue for issue in errors))


class ReplayTests(RepositoryFixture):
    def test_phase_c_requires_positive_native_delivery(self):
        name = f"{EVENTS}/evidence/retest/runtime-observations.jsonl"
        records = json_rows((ROOT / name).read_text())
        for record in records:
            if record["event"] == "scoped_delivery":
                record["native_positive_records"] = 0
        self.put(name, "\n".join(map(json.dumps, records)))
        with self.assertRaisesRegex(ValueError, "positive native control"):
            check_event_retest(self.repo())


class CatalogTests(RepositoryFixture):
    def test_requirement_to_boundary_drift_fails(self):
        for name in (RISK_FILE, WORK_FILE, PROJECT_FILE):
            self.put(name, (ROOT / name).read_text())
        for source in (ROOT / DESIGN).rglob("*.md"):
            self.put(source.relative_to(ROOT).as_posix(), source.read_text())
        trace = f"{DESIGN}/microtasks/requirements-traceability.md"
        document = (ROOT / trace).read_text()
        original = "| 1 · Browser to application | REQ-03, REQ-09 "
        self.assertIn(original, document)
        self.put(trace, document.replace(original, "| 1 · Browser to application | REQ-03, REQ-08 "))
        _, errors = check_catalog(self.repo())
        self.assertTrue(any("Boundary 1" in issue for issue in errors))


class WorkflowTests(RepositoryFixture):
    def test_rejects_write_permissions_privileged_trigger_and_unpinned_action(self):
        fast = (ROOT / FAST).read_text()
        self.put(FAST, fast.replace("contents: read", "contents: write")
                 .replace("pull_request:", "pull_request_target:")
                 .replace(ACTIONS["actions/checkout"], "v5"))
        self.put(MANUAL, (ROOT / MANUAL).read_text())
        _, errors = check_configuration(self.repo())
        self.assertTrue(any("permissions" in issue for issue in errors))
        self.assertTrue(any("trigger" in issue for issue in errors))
        self.assertTrue(any("pin list" in issue for issue in errors))

    def test_requires_explicit_and_protected_integration_gate(self):
        self.put(FAST, (ROOT / FAST).read_text())
        self.put(MANUAL, (ROOT / MANUAL).read_text().replace(GUARD, "always()"))
        _, errors = check_configuration(self.repo())
        self.assertTrue(any("isolation guards" in issue for issue in errors))

    def test_unavailable_docker_blocks_manual_integration_without_downloads(self):
        docker = self.put("bin/docker", "#!/usr/bin/env bash\nprintf '%s\\n' \"$*\" >> \"$P006_TEST_CALLS\"\nexit 1\n")
        docker.chmod(0o755)
        calls = self.root / "calls"
        output = self.root / "output"
        env = {**os.environ, "PATH": str(docker.parent) + os.pathsep + os.environ["PATH"], "P006_TEST_CALLS": str(calls)}
        argv = ["bash", str(ROOT / "scripts/verification/run-integration.sh"), "--confirm-isolated", str(output)]
        result = subprocess.run(argv, cwd=ROOT, env=env, capture_output=True, text=True, check=False)
        self.assertEqual(result.returncode, 2)
        if calls.exists():
            self.assertEqual(calls.read_text().splitlines(), ["info"])
        summary = json.loads((output / "integration.json").read_text())
        self.assertEqual(summary["status"], "BLOCKED")
        self.assertEqual(summary["req07"]["status"], "NOT_TESTED")
        self.assertEqual(summary["req08"]["status"], "NOT_TESTED")


class ResultTests(unittest.TestCase):
    def test_actual_failure_takes_precedence_over_missing_prerequisite(self):
        report = Report()
        report.checks = [{"status": "NOT_TESTED"}, {"status": "BLOCKED"}]
        self.assertEqual(report.result(), ("BLOCKED", 2))
        report.checks.append({"status": "FAIL"})
        self.assertEqual(report.result(), ("FAIL", 1))


if __name__ == "__main__":
    unittest.main()
