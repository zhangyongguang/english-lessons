"""Shared helpers: repo root, date parsing, JSON loading, and table/TSV escaping.

Pure standard library. Imported by the other scripts so the two subsystems
(errors / vocab) share one implementation of the fiddly bits.
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Error log is sharded: data/errors/{json,md}/YYYY-MM/YYYY-MM-DD.{json,md}
ERRORS_DIR = ROOT / "data" / "errors"
ERRORS_JSON_DIR = ERRORS_DIR / "json"
ERRORS_MD_DIR = ERRORS_DIR / "md"


def month_of(date_str: str) -> str:
    """'2026-05-28' -> '2026-05' (the year-month folder a day belongs to)."""
    return str(date_str)[:7]


def error_json_path(date_str: str) -> Path:
    """Path to a day's structured errors: data/errors/json/YYYY-MM/YYYY-MM-DD.json"""
    return ERRORS_JSON_DIR / month_of(date_str) / f"{date_str}.json"


def error_md_path(date_str: str) -> Path:
    """Path to a day's readable report: data/errors/md/YYYY-MM/YYYY-MM-DD.md"""
    return ERRORS_MD_DIR / month_of(date_str) / f"{date_str}.md"


def error_json_files():
    """Every error JSON file (recursive, sorted), excluding *.example.json."""
    if not ERRORS_JSON_DIR.exists():
        return []
    return sorted(
        p for p in ERRORS_JSON_DIR.rglob("*.json")
        if not p.name.endswith(".example.json")
    )


def parse_date(filename: str):
    """Extract the class date from a filename, returning 'YYYY-MM-DD', or None if not found.

    Tencent Meeting filenames look like:
      1780031783648_20260528210658-Transcription_...-1.txt
                     ^^^^^^^^^^^^^^  = YYYYMMDDhhmmss
    """
    m = re.search(r"_(\d{8})\d{6}-", filename)
    if not m:
        m = re.search(r"(\d{8})\d{6}", filename)  # fallback
    if not m:
        return None
    d = m.group(1)
    return f"{d[0:4]}-{d[4:6]}-{d[6:8]}"


def read_json(path, default=None):
    """Read JSON from `path`.

    Missing or empty/whitespace-only file -> `default`. Malformed JSON raises
    json.JSONDecodeError so the caller can report which file is broken.
    """
    try:
        text = Path(path).read_text(encoding="utf-8")
    except FileNotFoundError:
        return default
    if not text.strip():
        return default
    return json.loads(text)


def as_records(data):
    """Normalize loaded JSON to a list of record dicts.

    None -> []; a single dict -> [dict]; a list stays a list.
    """
    if data is None:
        return []
    if isinstance(data, dict):
        return [data]
    return list(data)


def md_cell(text):
    """Make text safe inside a Markdown table cell: escape pipes, flatten newlines."""
    return str(text).replace("|", "\\|").replace("\n", " ").strip()


def tsv_clean(text):
    """Make text safe inside a TSV cell: tabs -> space, newlines -> <br>."""
    return str(text).replace("\t", " ").replace("\n", "<br>")
