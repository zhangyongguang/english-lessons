"""Shared helpers: locate the repo root, parse the date from a Tencent transcript filename."""
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
