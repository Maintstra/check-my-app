import json
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class PublicExampleTests(unittest.TestCase):
    def test_mobile_source_only_example_validates_without_claiming_device_pass(self):
        path = ROOT / "examples" / "mobile-source-only" / "report.json"
        report = json.loads(path.read_text(encoding="utf-8"))
        result = subprocess.run(
            [sys.executable, str(ROOT / "skill/check-my-app/scripts/validate_report.py"), str(path)],
            capture_output=True, text=True, check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(report["verdict"], "Not ready")
        for journey in report["scope"]["journeys"]:
            self.assertTrue(journey["required"])
            self.assertEqual(journey["result"], "untested")
            claim = next(c for c in report["claims"] if c["id"] == journey["claimId"])
            self.assertEqual(claim["status"], "untested")
            self.assertEqual(claim["evidenceIds"], [])
        self.assertEqual(report["externalEffects"]["observed"], [])


if __name__ == "__main__":
    unittest.main()
