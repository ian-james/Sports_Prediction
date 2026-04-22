import os
import tempfile
from pathlib import Path

import yaml


def save_yaml(data, file_path):
    """Atomic write: writes to temp file first, then moves to destination."""
    path = Path(file_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    fd, temp_path = tempfile.mkstemp(dir=path.parent, suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            yaml.safe_dump(data, f, default_flow_style=False)
        os.replace(temp_path, file_path)
    except Exception as e:
        if os.path.exists(temp_path):
            os.remove(temp_path)
        print(f"Failed to save YAML: {e}")


def load_yaml(file_path):
    """Loads YAML and returns a dict. Returns empty dict if file missing."""
    path = Path(file_path)
    if not path.exists():
        return {}
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}
