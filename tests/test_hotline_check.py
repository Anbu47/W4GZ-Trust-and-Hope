import importlib.util
import json
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("checker", ROOT / "scripts/check_hotlines.py")
checker = importlib.util.module_from_spec(spec)
spec.loader.exec_module(checker)


class HotlineChecks(unittest.TestCase):
    def fixture(self):
        _, cards = checker.read_support(ROOT / "index.html")
        directory = []
        pages = {}
        hours = {"mai": "1:00 PM to 8:30 PM every Wednesday to Sunday", "hope": "Vietnamese and English", "child": "24/7", "csaga": "8:00 a.m. to 9:00 p.m.", "peace": "24/7"}
        for ident, (title, alias, slug, host) in checker.PROFILES.items():
            card = next(c for c in cards if c["title"].startswith(title))
            url = "https://findahelpline.com/organizations/" + slug
            directory.append('<article><a href="' + url + '">' + alias + '</a><p>' + ' / '.join(card["phones"]) + '</p></article>')
            pages[url] = '<h1>' + title + '</h1><a href="https://' + host + '">Official website</a><p>' + hours[ident] + '</p>'
        pages[checker.DIRECTORY] = ''.join(directory)
        return pages

    def test_all_five_contacts_match(self):
        report = checker.verify(ROOT / "index.html", self.fixture().__getitem__)
        self.assertEqual(report["status"], "passed")
        self.assertEqual(len(report["checks"]), 5)
        self.assertEqual(report["checks"][1]["hours"], "not_published_in_profile")

    def test_changed_phone_fails(self):
        pages = self.fixture()
        pages[checker.DIRECTORY] = pages[checker.DIRECTORY].replace('+84963061414', '+84963060000')
        report = checker.verify(ROOT / "index.html", pages.__getitem__)
        self.assertEqual(report["status"], "needs_review")
        self.assertIn("Phone number changed or missing: mai", report["issues"])

    def test_phone_under_wrong_provider_does_not_pass(self):
        pages = self.fixture()
        pages[checker.DIRECTORY] = pages[checker.DIRECTORY].replace('+84963061414', '000000000').replace('0865044400', '0865044400 +84963061414')
        report = checker.verify(ROOT / "index.html", pages.__getitem__)
        self.assertEqual(report["status"], "needs_review")

    def test_changed_hours_fail(self):
        pages = self.fixture()
        url = 'https://findahelpline.com/organizations/' + checker.PROFILES['csaga'][2]
        pages[url] = pages[url].replace('9:00 p.m.', '6:00 p.m.')
        self.assertEqual(checker.verify(ROOT / "index.html", pages.__getitem__)["status"], "needs_review")

    def test_missing_listing_cannot_be_verified(self):
        pages = self.fixture()
        pages[checker.DIRECTORY] = '<p>Unavailable</p>'
        with self.assertRaises(ValueError):
            checker.verify(ROOT / "index.html", pages.__getitem__)

    def test_failure_keeps_last_success_date(self):
        previous = {"run_number": 1, "last_verified_at": "2026-11-16T00:00:00+00:00", "last_verified_support_sha256": "old-hash"}
        responses = [{}, {"sha": "blob", "content": checker.base64.b64encode(json.dumps(previous).encode()).decode()}, {}]
        report = {"run_number": 2, "status": "needs_review", "checked_at": "2026-11-18T00:00:00+00:00", "support_sha256": "new-hash"}
        with patch.object(checker, "github", side_effect=responses):
            checker.publish(report)
        self.assertEqual(report["last_verified_at"], previous["last_verified_at"])

    def test_old_run_cannot_replace_newer_result(self):
        previous = {"run_number": 10}
        responses = [{}, {"sha": "blob", "content": checker.base64.b64encode(json.dumps(previous).encode()).decode()}]
        with patch.object(checker, "github", side_effect=responses) as api:
            checker.publish({"run_number": 2, "status": "passed"})
        self.assertEqual(api.call_count, 2)


if __name__ == "__main__":
    unittest.main()
