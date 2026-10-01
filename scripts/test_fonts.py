import subprocess, sys, unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

class FontsTest(unittest.TestCase):
    def run_check(self):
        return subprocess.run([sys.executable, "scripts/check_fonts.py"], cwd=ROOT,
                              capture_output=True, text=True)

    def test_every_face_present_and_covering(self):
        r = self.run_check()
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)

    def test_magazine_face_declared(self):
        css = (ROOT / "fonts.css").read_text()
        self.assertIn("font-family: 'Fira Sans Condensed'", css)

    def test_literata_retired(self):
        self.assertNotIn("Literata", (ROOT / "fonts.css").read_text())
        self.assertEqual(list((ROOT / "fonts").glob("literata-*")), [])

if __name__ == "__main__":
    unittest.main()
