"""共用工具：定位仓库根目录、从腾讯转写文件名里解析日期。"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def parse_date(filename: str):
    """从文件名里抽出上课日期，返回 'YYYY-MM-DD'，解析不到返回 None。

    腾讯会议文件名形如:
      1780031783648_20260528210658-Transcription_...-逐字稿文本-1.txt
                     ^^^^^^^^^^^^^^  = 年月日时分秒
    """
    m = re.search(r"_(\d{8})\d{6}-", filename)
    if not m:
        m = re.search(r"(\d{8})\d{6}", filename)  # 兜底
    if not m:
        return None
    d = m.group(1)
    return f"{d[0:4]}-{d[4:6]}-{d[6:8]}"
