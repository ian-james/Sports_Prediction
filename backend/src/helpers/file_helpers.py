from pathlib import Path


def ensure_dir(path: str) -> str:
    Path(path).mkdir(parents=True, exist_ok=True)
    return path


def generate_path(base_path, year, team, filename, ext="csv"):
    """Generates a nested path and ensures the parent directory exists."""
    full_path = Path(base_path) / str(year) / team / f"{filename}.{ext}"
    full_path.parent.mkdir(parents=True, exist_ok=True)
    return full_path
