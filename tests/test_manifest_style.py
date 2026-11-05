"""Style checker exceptions for FQL quotes and APT actor names."""

from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path


def _load_validator():
    path = Path(__file__).resolve().parents[1] / "scripts" / "validate-manifests.py"
    spec = importlib.util.spec_from_file_location("validate_manifests", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class StyleCheckTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.mod = _load_validator()

    def _errors(self, text: str) -> list[str]:
        report = self.mod.Report()
        self.mod.style_text(report, "sample", text)
        return report.errors

    def test_fql_single_quotes_in_code_and_literals_pass(self) -> None:
        text = "Use `merged.value = 'true'` and status = 'Open' for APT29 or APT-29.\n"
        self.assertEqual(self._errors(text), [])

    def test_prose_contraction_and_bare_apt_fail(self) -> None:
        errors = self._errors("Don't ship the APT name.\n")
        self.assertTrue(any("apostrophe" in error for error in errors))
        self.assertTrue(any("retired product name" in error for error in errors))

    def test_em_dash_still_fails(self) -> None:
        errors = self._errors("Leave it — then stop.\n")
        self.assertTrue(any("em dash" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
