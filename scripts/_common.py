"""Shared helpers: repo root, date parsing, JSON loading, and table/TSV escaping.

Pure standard library. Imported by the other scripts so the two subsystems
(errors / vocab) share one implementation of the fiddly bits.
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


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
