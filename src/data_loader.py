import json
import pandas as pd


def load_jsonl(file_path: str) -> pd.DataFrame:
    """Load JSONL dengan validasi baris rusak."""
    data = []
    with open(file_path, "r", encoding="utf-8") as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            try:
                data.append(json.loads(line))
            except json.JSONDecodeError as e:
                print(f"[WARN] Baris {line_num} gagal di-parse: {e}")
    return pd.DataFrame(data)
