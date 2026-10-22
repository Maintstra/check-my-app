import copy
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = ROOT / "skill" / "check-my-app" / "scripts" / "validate_report.py"
SCHEMA = ROOT / "skill" / "check-my-app" / "references" / "report-schema-v1.json"
SCHEMA_V1_1 = ROOT / "skill" / "check-my-app" / "references" / "report-schema-v1.1.json"
FIXTURES = ROOT / "tests" / "fixtures"


class ReportValidatorTests(unittest.TestCase):
    def run_validator(self, report):
        self.assertTrue(VALIDATOR.exists(), "report validator has not been implemented")
        with tempfile.TemporaryDirectory() as directory:
            report_path = Path(directory) / "report.json"
            report_path.write_text(json.dumps(report), encoding="utf-8")
            return subprocess.run(
                [sys.executable, str(VALIDATOR), str(report_path)],
                capture_output=True,
                text=True,
                check=False,
            )

    def load(self, name="valid-audit-report.json"):
        return json.loads((FIXTURES / name).read_text(encoding="utf-8"))

    def assert_rejected(self, report, code):
        result = self.run_validator(report)
        self.assertNotEqual(result.returncode, 0, result.stdout)
        self.assertIn(code, result.stderr)

    def test_versioned_schema_exists(self):
        self.assertTrue(SCHEMA.exists(), "versioned report schema has not been implemented")
        self.assertTrue(SCHEMA_V1_1.exists(), "closure report schema has not been implemented")

    def test_v1_1_schema_encodes_the_closure_gate(self):
        schema = json.loads(SCHEMA_V1_1.read_text(encoding="utf-8"))
        boundary = schema["$defs"]["closure"]["properties"]["boundary"]
        self.assertEqual(
            set(boundary["required"]),
            {
                "capabilities",
                "roles",
                "surfaces",
                "personas",
                "configurations",
                "lifecycleStages",
                "safetyBoundaries",
            },
        )
        self.assertIn("artifactSha256", schema["$defs"]["closurePass"]["required"])
        self.assertGreaterEqual(len(schema["allOf"]), 3)

    def test_valid_report_is_accepted(self):
        result = self.run_validator(self.load())
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("VALID check-my-app-report@1.0.0", result.stdout)

    def test_valid_delivery_closure_report_is_accepted(self):
        result = self.run_validator(self.load("valid-delivery-closure-report.json"))
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("VALID check-my-app-report@1.1.0", result.stdout)

    def test_delivery_closure_requires_two_clean_full_passes(self):
        report = self.load("valid-delivery-closure-report.json")
        report["closure"]["passes"] = report["closure"]["passes"][:1]
        report["closure"]["cleanPassCount"] = 1
        self.assert_rejected(report, "CLOSURE_CLEAN_PASSES_REQUIRED")

    def test_delivery_closure_requires_at_least_two_journeys(self):
        report = self.load("valid-delivery-closure-report.json")
        report["scope"]["journeys"] = report["scope"]["journeys"][:1]
        for items in report["closure"]["boundary"].values():
            for item in items:
                item["journeyIds"] = ["J1"]
        for closure_pass in report["closure"]["passes"]:
            closure_pass["journeyResults"] = closure_pass["journeyResults"][:1]
        self.assert_rejected(report, "CLOSURE_JOURNEY_MATRIX_REQUIRED")

    def test_delivery_closure_rejects_optional_placeholder_journey(self):
        report = self.load("valid-delivery-closure-report.json")
        report["scope"]["journeys"][1]["required"] = False
        report["scope"]["journeys"][1]["result"] = "untested"
        for items in report["closure"]["boundary"].values():
            for item in items:
                item["journeyIds"] = ["J1"]
        for closure_pass in report["closure"]["passes"]:
            closure_pass["journeyResults"][1]["result"] = "untested"
        self.assert_rejected(report, "CLOSURE_JOURNEY_MATRIX_REQUIRED")

    def test_delivery_closure_requires_every_required_journey_in_each_clean_pass(self):
        report = self.load("valid-delivery-closure-report.json")
        report["closure"]["passes"][-1]["journeyResults"] = [
            {"journeyId": "J1", "result": "passed"}
        ]
        self.assert_rejected(report, "CLOSURE_REQUIRED_JOURNEY_MISSING")

    def test_delivery_closure_rejects_failed_required_journey(self):
        report = self.load("valid-delivery-closure-report.json")
        report["scope"]["journeys"][1]["result"] = "failed"
        self.assert_rejected(report, "DELIVERY_REQUIRED_JOURNEY_FAILED")

    def test_delivery_closure_rejects_open_must_fix_finding(self):
        report = self.load("valid-delivery-closure-report.json")
        report["findings"][0]["status"] = "open"
        self.assert_rejected(report, "VERDICT_MUST_FIX_CONFLICT")

    def test_delivery_closure_rejects_artifact_mismatch(self):
        report = self.load("valid-delivery-closure-report.json")
        report["closure"]["passes"][-1]["artifactIdentity"] = "older-installer"
        self.assert_rejected(report, "CLOSURE_ARTIFACT_MISMATCH")

    def test_delivery_closure_rejects_new_material_finding_in_clean_pass(self):
        report = self.load("valid-delivery-closure-report.json")
        report["closure"]["passes"][-1]["newFindingIds"] = ["F1"]
        self.assert_rejected(report, "CLOSURE_MATERIAL_FINDING_DISCOVERED")

    def test_delivery_closure_requires_boundary_mapping(self):
        report = self.load("valid-delivery-closure-report.json")
        report["closure"]["boundary"]["surfaces"][0]["journeyIds"] = []
        self.assert_rejected(report, "CLOSURE_BOUNDARY_MAPPING_REQUIRED")

    def test_delivery_closure_required_boundary_maps_only_to_required_journeys(self):
        report = self.load("valid-delivery-closure-report.json")
        report["scope"]["journeys"].append(
            {"id": "J3", "name": "Optional export", "required": False, "result": "failed", "claimId": "C2"}
        )
        for closure_pass in report["closure"]["passes"]:
            closure_pass["journeyResults"].append({"journeyId": "J3", "result": "failed"})
        report["closure"]["boundary"]["capabilities"][0]["journeyIds"] = ["J3"]
        self.assert_rejected(report, "CLOSURE_BOUNDARY_REQUIRED_JOURNEY")

    def test_delivery_closure_rejects_all_excluded_boundary(self):
        report = self.load("valid-delivery-closure-report.json")
        for items in report["closure"]["boundary"].values():
            for item in items:
                item["disposition"] = "excluded"
                item["journeyIds"] = []
        self.assert_rejected(report, "CLOSURE_BOUNDARY_REQUIRED_COVERAGE")

    def test_delivery_closure_requires_all_boundary_dimensions(self):
        report = self.load("valid-delivery-closure-report.json")
        report["closure"]["boundary"]["personas"] = []
        self.assert_rejected(report, "CLOSURE_BOUNDARY_REQUIRED")

    def test_delivery_closure_requires_independent_evidence_for_clean_passes(self):
        report = self.load("valid-delivery-closure-report.json")
        report["closure"]["passes"][-1]["evidenceIds"] = ["E3"]
        self.assert_rejected(report, "CLOSURE_PASS_EVIDENCE_REUSED")

    def test_delivery_closure_requires_artifact_sha256(self):
        report = self.load("valid-delivery-closure-report.json")
        del report["product"]["artifact"]["sha256"]
        self.assert_rejected(report, "CLOSURE_ARTIFACT_SHA256_REQUIRED")

    def test_delivery_closure_rejects_artifact_sha256_mismatch(self):
        report = self.load("valid-delivery-closure-report.json")
        report["closure"]["passes"][-1]["artifactSha256"] = "b" * 64
        self.assert_rejected(report, "CLOSURE_ARTIFACT_MISMATCH")

    def test_delivery_closure_rejects_unknown_pass_field(self):
        report = self.load("valid-delivery-closure-report.json")
        report["closure"]["passes"][-1]["unverifiedNote"] = "looks good"
        self.assert_rejected(report, "CLOSURE_PASS_UNKNOWN_FIELD")

    def test_v1_1_rejects_unknown_artifact_field(self):
        report = self.load("valid-delivery-closure-report.json")
        report["product"]["artifact"]["unverifiedLabel"] = "same artifact"
        self.assert_rejected(report, "ARTIFACT_UNKNOWN_FIELD")

    def test_malformed_mode_returns_stable_error(self):
        report = self.load("valid-delivery-closure-report.json")
        report["mode"] = ["Delivery Closure"]
        result = self.run_validator(report)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("MODE_INVALID", result.stderr)
        self.assertNotIn("Traceback", result.stderr)

    def test_v1_report_preserves_legacy_delivery_behavior(self):
        report = self.load()
        report["mode"] = "Release Gate"
        report["verdict"] = "Delivery ready"
        report["product"]["artifact"]["kind"] = "packaged-installer"
        report["findings"][0]["severity"] = "Improve"
        report["release"] = {
            "packagedJourneyTested": True,
            "cleanMachineTested": True,
            "installTested": True,
            "restartTested": True,
            "uninstallTested": True,
        }
        result = self.run_validator(report)
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_missing_root_cause_is_rejected(self):
        report = self.load()
        del report["findings"][0]["rootCause"]
        self.assert_rejected(report, "FINDING_REQUIRED_FIELD")

    def test_missing_retest_is_rejected(self):
        report = self.load()
        del report["findings"][0]["retest"]
        self.assert_rejected(report, "FINDING_REQUIRED_FIELD")

    def test_confirmed_claim_without_evidence_is_rejected(self):
        report = self.load()
        report["claims"][0]["evidenceIds"] = []
        self.assert_rejected(report, "CONFIRMED_CLAIM_EVIDENCE_REQUIRED")

    def test_vague_recommendation_fixture_is_rejected(self):
        self.assert_rejected(
            self.load("invalid-vague-recommendation.json"),
            "FINDING_RECOMMENDATION_TOO_VAGUE",
        )

    def test_unknown_evidence_reference_is_rejected(self):
        report = self.load()
        report["findings"][0]["evidenceIds"] = ["E404"]
        self.assert_rejected(report, "EVIDENCE_REFERENCE_UNKNOWN")

    def test_blocking_finding_cannot_be_delivery_ready(self):
        report = self.load()
        report["verdict"] = "Delivery ready"
        report["findings"][0]["severity"] = "Blocking"
        self.assert_rejected(report, "VERDICT_BLOCKING_CONFLICT")

    def test_development_artifact_cannot_be_delivery_ready(self):
        self.assert_rejected(
            self.load("invalid-delivery-report.json"),
            "DELIVERY_EXACT_ARTIFACT_REQUIRED",
        )

    def test_clean_machine_evidence_is_required_for_delivery(self):
        report = self.load("invalid-delivery-report.json")
        report["product"]["artifact"]["kind"] = "packaged-installer"
        report["release"]["packagedJourneyTested"] = True
        self.assert_rejected(report, "DELIVERY_CLEAN_MACHINE_REQUIRED")

    def test_sensitive_key_is_rejected_without_echoing_value(self):
        report = self.load()
        canary = "secret-value-must-not-be-echoed"
        report["apiKey"] = canary
        result = self.run_validator(report)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("SENSITIVE_KEY", result.stderr)
        self.assertNotIn(canary, result.stderr + result.stdout)

    def test_unknown_top_level_field_is_rejected(self):
        report = self.load()
        report["debugMetadata"] = "not part of the public contract"
        self.assert_rejected(report, "REPORT_UNKNOWN_FIELD")

    def test_invalid_evidence_type_is_rejected(self):
        report = self.load()
        report["evidence"][0]["type"] = "model-opinion"
        self.assert_rejected(report, "EVIDENCE_TYPE_INVALID")

    def test_every_schema_evidence_type_is_accepted(self):
        schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
        evidence_types = schema["$defs"]["evidence"]["properties"]["type"]["enum"]
        for evidence_type in evidence_types:
            with self.subTest(evidence_type=evidence_type):
                report = self.load()
                report["evidence"][0]["type"] = evidence_type
                result = self.run_validator(report)
                self.assertEqual(result.returncode, 0, result.stderr)


if __name__ == "__main__":
    unittest.main()
