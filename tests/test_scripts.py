"""Zero-dependency unit tests for the helper scripts (standard-library unittest).

Read-only: every file touched here is a temporary file. The real data under
data/ is never written. Run with:  python -m unittest discover -s tests
"""
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

# Make scripts/ importable (it is not a package).
ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS))

import _common  # noqa: E402
import build_master  # noqa: E402
import make_anki  # noqa: E402
import make_vocab_anki  # noqa: E402
import render_vocab_md  # noqa: E402
import review_errors  # noqa: E402


class TestParseDate(unittest.TestCase):
    def test_tencent_filename(self):
        name = "1780031783648_20260528210658-Transcription_x-1.txt"
        self.assertEqual(_common.parse_date(name), "2026-05-28")

    def test_fallback_without_underscore_dash(self):
        self.assertEqual(_common.parse_date("20260528210658-x.txt"), "2026-05-28")

    def test_no_date(self):
        self.assertIsNone(_common.parse_date("notes.txt"))


class TestErrorPaths(unittest.TestCase):
    def test_month_of(self):
        self.assertEqual(_common.month_of("2026-05-28"), "2026-05")

    def test_error_json_path(self):
        p = _common.error_json_path("2026-05-28")
        self.assertEqual(p, _common.ERRORS_JSON_DIR / "2026-05" / "2026-05-28.json")

    def test_error_md_path(self):
        p = _common.error_md_path("2026-05-28")
        self.assertEqual(p, _common.ERRORS_MD_DIR / "2026-05" / "2026-05-28.md")

    def test_error_json_files_are_sharded_and_sorted(self):
        files = _common.error_json_files()
        self.assertTrue(files, "expected at least one error JSON file")
        for f in files:
            # Each file lives under json/YYYY-MM/ and ends in .json
            self.assertEqual(f.suffix, ".json")
            self.assertRegex(f.parent.name, r"^\d{4}-\d{2}$")
        self.assertEqual(files, sorted(files))


class TestReadJson(unittest.TestCase):
    def test_missing_returns_default(self):
        self.assertEqual(_common.read_json(ROOT / "nope.json", []), [])

    def test_empty_file_returns_default(self):
        with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as f:
            f.write("   \n")
            p = Path(f.name)
        try:
            self.assertEqual(_common.read_json(p, []), [])
        finally:
            p.unlink()

    def test_valid_json(self):
        with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as f:
            f.write('[{"a": 1}]')
            p = Path(f.name)
        try:
            self.assertEqual(_common.read_json(p), [{"a": 1}])
        finally:
            p.unlink()

    def test_bad_json_raises(self):
        with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as f:
            f.write("{not json}")
            p = Path(f.name)
        try:
            with self.assertRaises(json.JSONDecodeError):
                _common.read_json(p)
        finally:
            p.unlink()


class TestAsRecords(unittest.TestCase):
    def test_none(self):
        self.assertEqual(_common.as_records(None), [])

    def test_dict_wrapped(self):
        self.assertEqual(_common.as_records({"x": 1}), [{"x": 1}])

    def test_list_passthrough(self):
        self.assertEqual(_common.as_records([1, 2]), [1, 2])


class TestEscaping(unittest.TestCase):
    def test_md_cell_escapes_pipe_and_newline(self):
        self.assertEqual(_common.md_cell("a|b\nc "), "a\\|b c")

    def test_tsv_clean(self):
        self.assertEqual(_common.tsv_clean("a\tb\nc"), "a b<br>c")


class TestVocabOrdering(unittest.TestCase):
    def _order(self, data):
        ordered = sorted(enumerate(data), key=render_vocab_md.sort_key, reverse=True)
        return [e["word"] for _, e in ordered]

    def test_newest_first_same_day_tiebreak_by_index(self):
        data = [
            {"word": "older", "first_seen": "2026-05-27", "review": {"last_seen": "2026-05-27"}},
            {"word": "first_today", "first_seen": "2026-05-29", "review": {"last_seen": "2026-05-29"}},
            {"word": "last_today", "first_seen": "2026-05-29", "review": {"last_seen": "2026-05-29"}},
        ]
        self.assertEqual(self._order(data), ["last_today", "first_today", "older"])

    def test_first_example(self):
        self.assertEqual(render_vocab_md.first_example({"example": ["a", "b"]}), "a")
        self.assertEqual(render_vocab_md.first_example({"example": "solo"}), "solo")
        self.assertEqual(render_vocab_md.first_example({}), "")


class TestFlatten(unittest.TestCase):
    def test_examples_joined_and_review_flattened(self):
        rec = {
            "id": "2026-05-29-001", "date": "2026-05-29", "category": "grammar",
            "tag": "tense", "my_sentence": "a", "correction": "b", "explanation": "c",
            "correct_examples": ["e1", "e2"], "context": "ctx",
            "review": {"status": "new", "times_seen_again": 2, "last_reviewed": None},
            "source_ref": "line 1",
        }
        row = build_master.flatten(rec)
        self.assertEqual(row["correct_examples"], "e1 | e2")
        self.assertEqual(row["status"], "new")
        self.assertEqual(row["times_seen_again"], 2)
        self.assertEqual(row["review_count"], 0)
        self.assertEqual(row["incorrect_count"], 0)
        self.assertEqual(row["last_reviewed"], "")


class TestAnkiCards(unittest.TestCase):
    def test_error_card(self):
        row = {
            "my_sentence": "I goes", "correction": "I go", "explanation": "subject-verb",
            "correct_examples": "He goes | They go", "category": "grammar", "tag": "agreement",
        }
        front, back, tags = make_anki.build_card(row)
        self.assertIn("I goes", front)
        self.assertIn("I go", back)
        self.assertIn("subject-verb", back)
        self.assertEqual(tags, "grammar agreement")

    def test_vocab_card(self):
        entry = {
            "word": "eloquent", "pos": "adjective", "definition": "fluent and persuasive",
            "example": ["She is eloquent."], "synonyms": ["articulate"], "topic": "communication",
        }
        front, back, tags = make_vocab_anki.build_card(entry)
        self.assertIn("eloquent", front)
        self.assertIn("fluent and persuasive", back)
        self.assertIn("articulate", back)
        self.assertEqual(tags, "adjective communication")


class TestSentenceReview(unittest.TestCase):
    def setUp(self):
        self.tempdir = tempfile.TemporaryDirectory()
        self.path = Path(self.tempdir.name) / "2026-08-01.json"
        self.records = [
            {
                "id": "2026-08-01-001", "date": "2026-08-01", "category": "grammar",
                "tag": "agreement", "my_sentence": "He go.", "correction": "He goes.",
                "explanation": "Do not use the quoted word \"review\" here.", "correct_examples": [],
                "review": {"status": "new", "times_seen_again": 0, "last_reviewed": None},
            },
            {
                "id": "2026-08-01-002", "date": "2026-08-01", "category": "grammar",
                "tag": "agreement", "my_sentence": "It work.", "correction": "It works.",
                "explanation": "Use third-person singular agreement.", "correct_examples": [],
                "review": {"status": "new", "times_seen_again": 0, "last_reviewed": None},
            },
        ]
        self.path.write_text(json.dumps(self.records), encoding="utf-8")

    def tearDown(self):
        self.tempdir.cleanup()

    def _rows(self):
        return review_errors.load_records([self.path])

    def test_next_prefers_recurring_foundational_error(self):
        result = review_errors.next_record(self._rows(), review_errors.parse_day("2026-08-03"))
        self.assertEqual(result["status"], "ok")
        self.assertEqual(result["record"]["id"], "2026-08-01-002")
        self.assertEqual(result["recommendation"]["tag_occurrences"], 2)
        self.assertIn("foundational_pattern", result["recommendation"]["reasons"])

    def test_record_incorrect_updates_counts_and_schedule(self):
        before = self.path.read_text(encoding="utf-8")
        record = review_errors.record_result(
            self._rows(), "2026-08-01-001", "incorrect", review_errors.parse_day("2026-08-03")
        )
        after = self.path.read_text(encoding="utf-8")
        self.assertEqual(record["review"]["review_count"], 1)
        self.assertEqual(record["review"]["incorrect_count"], 1)
        self.assertEqual(record["review"]["correct_streak"], 0)
        self.assertEqual(record["review"]["next_review"], "2026-08-04")
        self.assertIn('"my_sentence": "It work."', after)
        self.assertEqual(before.count('"my_sentence"'), after.count('"my_sentence"'))

    def test_review_update_supports_compact_json(self):
        compact = json.dumps(self.records, separators=(",", ":"))
        updated = review_errors.replace_review_text(
            compact,
            "2026-08-01-001",
            {"status": "learning", "review_count": 1},
        )
        records = json.loads(updated)
        self.assertEqual(records[0]["review"]["review_count"], 1)
        self.assertEqual(records[1]["review"]["status"], "new")

    def test_mastery_requires_three_distinct_days(self):
        for day in ("2026-08-03", "2026-08-04", "2026-08-07"):
            review_errors.record_result(
                self._rows(), "2026-08-01-001", "correct", review_errors.parse_day(day)
            )
        record = self._rows()[0][0]
        self.assertEqual(record["review"]["status"], "mastered")
        self.assertEqual(record["review"]["correct_count"], 3)
        self.assertEqual(record["review"]["review_days"], ["2026-08-03", "2026-08-04", "2026-08-07"])

    def test_future_review_is_not_due(self):
        review_errors.record_result(
            self._rows(), "2026-08-01-001", "correct", review_errors.parse_day("2026-08-03")
        )
        result = review_errors.next_record(
            self._rows(), review_errors.parse_day("2026-08-03"), exclude="2026-08-01-002"
        )
        self.assertEqual(result["status"], "nothing_due")
        self.assertEqual(result["next_review"], "2026-08-04")


class TestValidateScriptOnRealData(unittest.TestCase):
    def test_validate_passes_read_only(self):
        # Runs the real validator against the committed data; must pass and write nothing.
        result = subprocess.run(
            [sys.executable, str(SCRIPTS / "validate.py")],
            capture_output=True, text=True,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)


if __name__ == "__main__":
    unittest.main()
