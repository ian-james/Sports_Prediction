from pathlib import Path


def ensure_dir(path: str) -> str:
    Path(path).mkdir(parents=True, exist_ok=True)
    return path


def generate_path(base_path, year, team, filename, ext="csv"):
    """Generates a nested path and ensures the parent directory exists."""
    full_path = Path(base_path) / str(year) / team / f"{filename}.{ext}"
    full_path.parent.mkdir(parents=True, exist_ok=True)
    return full_path


def load_read_file(relative_path_str):
    # Get the directory of the current test file
    base_path = Path(__file__).parent

    # Resolve the full path
    full_path = (base_path / relative_path_str).resolve()

    print(f"\nDEBUG: Attempting to open: {full_path}")

    if not full_path.exists():
        # List files in the parent directory to help debug
        print(f"DEBUG: Directory contents of {full_path.parent}:")
        if full_path.parent.exists():
            print(list(full_path.parent.glob("*")))
        else:
            print("Parent directory does not exist!")

    with open(full_path, "r", encoding="utf-8", errors="replace") as f:
        return f.read()
