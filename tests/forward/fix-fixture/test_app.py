import unittest
from pathlib import Path


class SaveFeedbackContract(unittest.TestCase):
    def test_save_result_is_accessible_and_specific(self):
        html = (Path(__file__).parent / "app.html").read_text(encoding="utf-8")
        self.assertIn('id="save-result" role="status"', html)
        self.assertIn("Saved locally. No external records were changed.", html)


if __name__ == "__main__":
    unittest.main()
