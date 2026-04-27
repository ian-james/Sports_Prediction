import pandas as pd

from src.sports.hockey.mappings.standardized_names import InternalStat

_ROLLING_STAT_COLS = [
    InternalStat.GOALS_FOR,
    InternalStat.GOALS_AGAINST,
    InternalStat.SHOTS_FOR,
    InternalStat.SHOTS_AGAINST,
    InternalStat.PDO,
    InternalStat.HITS,
    InternalStat.BLOCKS,
    InternalStat.FO_PCT,
]


def add_rolling_averages(
    df: pd.DataFrame, windows: list[int] = [5, 10]
) -> pd.DataFrame:
    """Adds rolling mean columns for key stats using only prior games."""
    df = df.copy()
    for stat in _ROLLING_STAT_COLS:
        col = stat.value
        if col not in df.columns:
            continue
        for window in windows:
            df[f"rolling_{window}_{col}"] = (
                df[col].shift(1).rolling(window, min_periods=1).mean()
            )
    return df


def add_home_away_splits(df: pd.DataFrame) -> pd.DataFrame:
    """Adds cumulative home and away win rates using only prior games."""
    df = df.copy()
    is_home = df[InternalStat.IS_HOME.value]
    won = df[InternalStat.WON.value].astype(float)

    home_won = won.where(is_home, other=float("nan"))
    away_won = won.where(~is_home, other=float("nan"))

    df["home_win_pct_cumul"] = home_won.expanding().mean().shift(1)
    df["away_win_pct_cumul"] = away_won.expanding().mean().shift(1)
    return df


def _compute_streak_series(won_series: pd.Series) -> pd.Series:
    """Returns running streak: positive for wins, negative for losses."""
    streak = []
    current = 0
    for w in won_series:
        if pd.isna(w):
            streak.append(0)
            continue
        if w:
            current = max(1, current + 1)
        else:
            current = min(-1, current - 1)
        streak.append(current)
    return pd.Series(streak, index=won_series.index)


def add_streak(df: pd.DataFrame) -> pd.DataFrame:
    """Adds win/loss streak and last-10 win count going into each game."""
    df = df.copy()
    won = df[InternalStat.WON.value]
    df["streak"] = _compute_streak_series(won).shift(1).fillna(0).astype(int)
    df["last_10_wins"] = (
        won.astype(int).shift(1).rolling(10, min_periods=1).sum().fillna(0).astype(int)
    )
    return df


def add_head_to_head(df: pd.DataFrame) -> pd.DataFrame:
    """Adds cumulative win rate vs each opponent using only prior meetings."""
    df = df.copy()
    won_col = InternalStat.WON.value
    opp_col = InternalStat.OPPONENT.value
    df["h2h_win_rate"] = df.groupby(opp_col)[won_col].transform(
        lambda x: x.astype(float).shift(1).expanding().mean()
    )
    return df


def build_features(df: pd.DataFrame) -> pd.DataFrame:
    """Runs all feature generation steps on a preprocessed single-team game log."""
    return (
        df.pipe(add_rolling_averages)
        .pipe(add_home_away_splits)
        .pipe(add_streak)
        .pipe(add_head_to_head)
    )
