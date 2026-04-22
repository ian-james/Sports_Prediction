from pathlib import Path
from .string_helpers import slugify


def build_team_filename_fast(path: str, year: str, team: str, parser="full", ext="csv"):
    base_dir = Path(path)
    full_path = base_dir / str(year) / parser / f"{team}.{ext}"
    return full_path


def build_team_filename(
    path: str, year: str, team: str, parser="full", ext="csv"
) -> Path:
    """
    Builds a clean, cross-platform path.
    Example: 2024, "Toronto Maple Leafs" -> ../data/2024/full/toronto-maple-leafs.csv
    """
    # 1. Clean the components
    clean_team = slugify(team)
    clean_parser = slugify(parser)

    # 2. Use Path for intelligent joining (handles slashes automatically)
    base_dir = Path(path)
    full_path = base_dir / str(year) / clean_parser / f"{clean_team}.{ext}"

    # 3. Optional: Create the directory immediately so it's ready for writing
    full_path.parent.mkdir(parents=True, exist_ok=True)

    return full_path
