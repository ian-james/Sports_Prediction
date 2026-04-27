import pandas as pd

from src.sports.hockey.mappings.standardized_names import InternalStat

_NUMERIC_STAT_COLS = [
    InternalStat.GOALS_FOR,
    InternalStat.GOALS_AGAINST,
    InternalStat.GOAL_DIFF,
    InternalStat.SHOTS_FOR,
    InternalStat.SHOTS_AGAINST,
    InternalStat.SHOT_DIFF,
    InternalStat.PDO,
    InternalStat.PDO_ADJ,
    InternalStat.SH_PCT,
    InternalStat.SV_PCT,
    InternalStat.FOW,
    InternalStat.FOL,
    InternalStat.FO_DIFF,
    InternalStat.FO_PCT,
    InternalStat.HITS,
    InternalStat.HITS_AGAINST,
    InternalStat.HIT_DIFF,
    InternalStat.BLOCKS,
    InternalStat.BLOCKS_AGAINST,
    InternalStat.BLOCK_DIFF,
]


def normalize_dates(df: pd.DataFrame) -> pd.DataFrame:
    """Ensures the date column is datetime64; drops rows with unparseable dates."""
    col = InternalStat.DATE.value
    if col not in df.columns:
        return df
    df = df.copy()
    df[col] = pd.to_datetime(df[col], errors="coerce")
    return df.dropna(subset=[col]).reset_index(drop=True)


def normalize_outcomes(df: pd.DataFrame) -> pd.DataFrame:
    """Drops rows with a null or empty result column."""
    col = InternalStat.RESULT.value
    if col not in df.columns:
        return df
    df = df.copy()
    mask = df[col].notna() & (df[col].astype(str).str.strip() != "")
    return df[mask].reset_index(drop=True)


def normalize_location(df: pd.DataFrame) -> pd.DataFrame:
    """Ensures the is_home column is boolean."""
    col = InternalStat.IS_HOME.value
    if col not in df.columns:
        return df
    df = df.copy()
    df[col] = df[col].astype(bool)
    return df


def handle_missing_data(df: pd.DataFrame) -> pd.DataFrame:
    """Coerces numeric stat columns to float and fills NaN with 0."""
    df = df.copy()
    for stat in _NUMERIC_STAT_COLS:
        col = stat.value
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0.0).astype(float)
    return df


def preprocess(df: pd.DataFrame) -> pd.DataFrame:
    """Orchestrates all preprocessing steps; input should be post-adapter.finalize()."""
    return (
        df.pipe(normalize_dates)
        .pipe(normalize_outcomes)
        .pipe(normalize_location)
        .pipe(handle_missing_data)
        .sort_values(InternalStat.DATE.value, ascending=True)
        .reset_index(drop=True)
    )
