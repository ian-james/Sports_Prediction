import time
from pathlib import Path
import pandas as pd

from .file_helpers import ensure_dir


def safe_load_csv(file_path, **kwargs):
    """Loads CSV if exists, otherwise returns empty DataFrame."""
    path = Path(file_path)
    if path.exists():
        return pd.read_csv(path, **kwargs)
    return pd.DataFrame()


def quick_export(df, name="export", folder="output"):
    """Quickly dump a dataframe to a dated CSV."""
    ensure_dir(folder)
    timestamp = time.strftime("%Y%m%d-%H%M")
    dest = Path(folder) / f"{name}_{timestamp}.csv"
    df.to_csv(dest, index=False)
    print(f"Exported to {dest}")


def change_column_names(df, column_name_mapping):
    df.rename(columns=column_name_mapping, inplace=True, errors="ignore")
    return df


def clean_df(df):
    """Standardizes column names and strips whitespace from strings."""
    # 1. Lowercase and snake_case headers
    df.columns = [c.lower().replace(" ", "_").strip() for c in df.columns]

    # 2. Strip whitespace from all string columns
    str_cols = df.select_dtypes(include=["object"]).columns
    df[str_cols] = df[str_cols].apply(
        lambda x: x.str.strip() if hasattr(x, "str") else x
    )

    return df
