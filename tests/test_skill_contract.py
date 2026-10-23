import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skill" / "check-my-app" / "SKILL.md"
AGENT_CONFIG = ROOT / "skill" / "check-my-app" / "agents" / "openai.yaml"
REFERENCES = ROOT / "skill" / "check-my-app" / "references"


class SkillContractTests(unittest.TestCase):
    def test_skill_has_discoverable_frontmatter_and_no_placeholders(self):
        text = SKILL.read_text(encoding="utf-8")
        self.assertTrue(text.startswith("---\nname: check-my-app\n"))
        description = re.search(r"^description:\s*(.+)$", text, re.MULTILINE)
        self.assertIsNotNone(description)
        self.assertTrue(description.group(1).startswith("Use when "))
        self.assertNotRegex(text, r"\b(?:TODO|TBD)\b")

    def test_skill_has_an_exact_version(self):
        text = SKILL.read_text(encoding="utf-8")
        self.assertIn('version: "1.3.1"', text)

    def test_skill_defines_modes_evidence_and_mutation_boundary(self):
        text = SKILL.read_text(encoding="utf-8")
        for phrase in (
            "Audit",
            "Fix & Retest",
            "Delivery Closure",
            "in any language",
            "Release Gate",
            "No evidence, no pass",
            "confirmed",
            "inference",
            "untested",
            "explicit authorization",
            "production writes",
        ):
            self.assertIn(phrase, text)

    def test_skill_routes_to_all_required_references(self):
        text = SKILL.read_text(encoding="utf-8")
        required = {
            "surface-routing.md",
            "human-experience.md",
            "agent-trust.md",
            "findings-and-report.md",
            "release-gate.md",
            "delivery-closure.md",
            "examples.md",
            "execution-control.md",
            "installed-reality.md",
        }
        for name in required:
            self.assertTrue((REFERENCES / name).exists(), name)
            self.assertIn(f"references/{name}", text)

    def test_report_validator_is_part_of_completion_gate(self):
        text = SKILL.read_text(encoding="utf-8")
        self.assertIn("scripts/validate_report.py", text)
        self.assertIn("check-my-app-report@1.1.0", text)

    def test_delivery_closure_defines_convergence_instead_of_single_journey_retest(self):
        text = SKILL.read_text(encoding="utf-8")
        closure = (REFERENCES / "delivery-closure.md").read_text(encoding="utf-8")
        self.assertIn("Do not reduce this request to `Fix & Retest`", text)
        self.assertIn("three rings", closure)
        self.assertIn("two consecutive full passes", closure)
        self.assertIn('Never say "all bugs are fixed."', closure)

    def test_validator_command_is_portable_from_target_repositories(self):
        text = SKILL.read_text(encoding="utf-8")
        self.assertIn("Resolve the validator path relative to this SKILL.md", text)

    def test_validated_machine_report_precedes_human_summary(self):
        text = SKILL.read_text(encoding="utf-8")
        self.assertIn("Required output contract", text)
        self.assertIn("Produce both outputs for every completed audit", text)
        self.assertIn("Validate the JSON report before presenting the human-facing summary", text)
        self.assertIn("Do not replace the required finding fields with a prose checklist", text)

    def test_installed_reality_gates_are_defined(self):
        gates = (REFERENCES / "installed-reality.md").read_text(encoding="utf-8")
        for phrase in (
            "Locale completeness",
            "native and operating-system surfaces",
            "Representative real-data shapes",
            "minimum window size",
            "125%, and 150%",
            "Information hierarchy",
            "1366×768",
            "Desktop control fallback",
            "_electron.launch",
            "never `confirmed`",
        ):
            self.assertIn(phrase, gates)

    def test_openai_metadata_is_current(self):
        text = AGENT_CONFIG.read_text(encoding="utf-8")
        self.assertIn('display_name: "Check My App"', text)
        self.assertIn("$check-my-app", text)

    def test_local_markdown_links_resolve(self):
        for document in [SKILL, *REFERENCES.glob("*.md")]:
            text = document.read_text(encoding="utf-8")
            for target in re.findall(r"\]\(([^)]+)\)", text):
                if "://" in target or target.startswith("#"):
                    continue
                path = target.split("#", 1)[0]
                self.assertTrue((document.parent / path).is_file(), f"{document}: {target}")


if __name__ == "__main__":
    unittest.main()
