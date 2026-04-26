import math

import pandas as pd
import pytest

from src.sports.hockey.features.quant_feature_pipeline import (
    add_head_to_head,
    add_home_away_splits,
    add_rolling_averages,
    add_streak,
    build_features,
)
from src.sports.hockey.mappings.standardized_names import InternalStat


def _game(
    date: str,
    opponent: str,
    won: bool,
    is_home: bool = True,
    goals_for: float = 3.0,
    goals_against: float = 1.0,
    shots_for: float = 30.0,
) -> dict:
    return {
        InternalStat.DATE.value: pd.Timestamp(date),
        InternalStat.OPPONENT.value: opponent,
        InternalStat.IS_HOME.value: is_home,
        InternalStat.RESULT.value: "Win" if won else "Loss",
        InternalStat.WON.value: won,
        InternalStat.OT_GAME.value: False,
        InternalStat.POINTS_EARNED.value: 2 if won else 0,
        InternalStat.GOALS_FOR.value: goals_for,
        InternalStat.GOALS_AGAINST.value: goals_against,
        InternalStat.SHOTS_FOR.value: shots_for,
        InternalStat.SHOTS_AGAINST.value: 25.0,
    }


def _make_df(games: list[dict]) -> pd.DataFrame:
    return pd.DataFrame(games)


class TestRollingAverages:
    def test_rolling_columns_created(self):
        df = _make_df([_game("2025-10-01", "A", True)] * 6)
        result = add_rolling_averages(df)
        assert f"rolling_5_{InternalStat.GOALS_FOR.value}" in result.columns
        assert f"rolling_10_{InternalStat.GOALS_FOR.value}" in result.columns

    def test_first_row_is_nan_no_prior_games(self):
        df = _make_df([_game("2025-10-01", "A", True, goals_for=3.0)] * 6)
        result = add_rolling_averages(df, windows=[5])
        assert math.isnan(result[f"rolling_5_{InternalStat.GOALS_FOR.value}"].iloc[0])

    def test_rolling_uses_prior_games_only(self):
        games = [
            _game(f"2025-10-0{i+1}", "A", True, goals_for=float(i + 1))
            for i in range(6)
        ]
        df = _make_df(games)
        result = add_rolling_averages(df, windows=[3])
        col = f"rolling_3_{InternalStat.GOALS_FOR.value}"
        # Row 3: prior games are rows 0(1), 1(2), 2(3) → mean=2.0
        assert result[col].iloc[3] == pytest.approx(2.0)
        # Row 5: prior games rows 2(3), 3(4), 4(5) → mean=4.0
        assert result[col].iloc[5] == pytest.approx(4.0)

    def test_custom_windows_respected(self):
        df = _make_df([_game("2025-10-01", "A", True)] * 5)
        result = add_rolling_averages(df, windows=[3])
        assert f"rolling_3_{InternalStat.GOALS_FOR.value}" in result.columns
        assert f"rolling_5_{InternalStat.GOALS_FOR.value}" not in result.columns


class TestHomeAwaySplits:
    def test_columns_created(self):
        games = [
            _game("2025-10-01", "A", True, is_home=True),
            _game("2025-10-03", "B", False, is_home=False),
        ]
        result = add_home_away_splits(_make_df(games))
        assert "home_win_pct_cumul" in result.columns
        assert "away_win_pct_cumul" in result.columns

    def test_first_game_has_nan_split(self):
        games = [_game("2025-10-01", "A", True, is_home=True)]
        result = add_home_away_splits(_make_df(games))
        assert math.isnan(result["home_win_pct_cumul"].iloc[0])

    def test_home_win_pct_accumulates_correctly(self):
        games = [
            _game("2025-10-01", "A", True, is_home=True),  # home win
            _game(
                "2025-10-03", "B", False, is_home=False
            ),  # away loss (ignored for home)
            _game("2025-10-05", "C", False, is_home=True),  # home loss
            _game(
                "2025-10-07", "D", True, is_home=True
            ),  # home win → before: 1W/2G = 0.5
        ]
        result = add_home_away_splits(_make_df(games))
        assert result["home_win_pct_cumul"].iloc[3] == pytest.approx(0.5)

    def test_split_values_in_valid_range(self):
        games = [
            _game(f"2025-10-0{i+1}", "A", i % 2 == 0, is_home=i % 2 == 0)
            for i in range(6)
        ]
        result = add_home_away_splits(_make_df(games))
        valid = result["home_win_pct_cumul"].dropna()
        assert (valid >= 0).all() and (valid <= 1).all()


class TestStreak:
    def test_streak_column_created(self):
        df = _make_df([_game("2025-10-01", "A", True)])
        result = add_streak(df)
        assert "streak" in result.columns
        assert "last_10_wins" in result.columns

    def test_first_game_streak_is_zero(self):
        df = _make_df([_game("2025-10-01", "A", True)])
        result = add_streak(df)
        assert result["streak"].iloc[0] == 0

    def test_positive_streak_after_win_run(self):
        games = [
            _game("2025-10-01", "A", True),
            _game("2025-10-03", "B", True),
            _game("2025-10-05", "C", True),
            _game("2025-10-07", "D", False),  # going into this game: 3-win streak
        ]
        result = add_streak(_make_df(games))
        assert result["streak"].iloc[3] == 3

    def test_negative_streak_after_loss_run(self):
        games = [
            _game("2025-10-01", "A", False),
            _game("2025-10-03", "B", False),
            _game("2025-10-05", "C", True),  # going into this game: 2-loss streak
        ]
        result = add_streak(_make_df(games))
        assert result["streak"].iloc[2] == -2

    def test_streak_resets_on_result_change(self):
        games = [
            _game("2025-10-01", "A", True),
            _game("2025-10-03", "B", False),  # streak resets → going in: +1
            _game("2025-10-05", "C", True),  # going in: -1 (one loss)
        ]
        result = add_streak(_make_df(games))
        assert result["streak"].iloc[1] == 1
        assert result["streak"].iloc[2] == -1

    def test_last_10_wins_counts_prior_games(self):
        # 6 wins followed by 4 losses → at the 11th game, last_10_wins should be 6
        games = [_game(f"2025-10-{i+1:02d}", "A", True) for i in range(6)] + [
            _game(f"2025-11-{i+1:02d}", "A", False) for i in range(5)
        ]
        result = add_streak(_make_df(games))
        assert result["last_10_wins"].iloc[10] == 6


class TestHeadToHead:
    def test_column_created(self):
        df = _make_df([_game("2025-10-01", "Rangers", True)])
        result = add_head_to_head(df)
        assert "h2h_win_rate" in result.columns

    def test_first_meeting_is_nan(self):
        df = _make_df([_game("2025-10-01", "Rangers", True)])
        result = add_head_to_head(df)
        assert math.isnan(result["h2h_win_rate"].iloc[0])

    def test_second_meeting_reflects_first_result(self):
        games = [
            _game("2025-10-01", "Rangers", True),  # win vs Rangers
            _game("2025-10-03", "Rangers", False),  # going in: 1 win / 1 game = 1.0
        ]
        result = add_head_to_head(_make_df(games))
        assert result["h2h_win_rate"].iloc[1] == pytest.approx(1.0)

    def test_h2h_is_opponent_specific(self):
        games = [
            _game("2025-10-01", "Rangers", True),
            _game("2025-10-03", "Bruins", False),  # first meeting vs Bruins → NaN
            _game("2025-10-05", "Rangers", False),  # second vs Rangers → 1.0
        ]
        result = add_head_to_head(_make_df(games))
        assert math.isnan(result["h2h_win_rate"].iloc[1])
        assert result["h2h_win_rate"].iloc[2] == pytest.approx(1.0)

    def test_h2h_accumulates_over_multiple_meetings(self):
        games = [
            _game("2025-10-01", "Rangers", True),  # W
            _game("2025-10-05", "Rangers", True),  # W  → going in: 1.0
            _game("2025-10-10", "Rangers", False),  # L  → going in: 1.0
            _game("2025-10-15", "Rangers", True),  # W  → going in: 2W/3G = 0.667
        ]
        result = add_head_to_head(_make_df(games))
        assert result["h2h_win_rate"].iloc[3] == pytest.approx(2 / 3)


class TestBuildFeatures:
    def test_all_feature_groups_present(self):
        games = [_game(f"2025-10-{i+1:02d}", "A", i % 2 == 0) for i in range(12)]
        result = build_features(_make_df(games))
        assert f"rolling_5_{InternalStat.GOALS_FOR.value}" in result.columns
        assert "home_win_pct_cumul" in result.columns
        assert "streak" in result.columns
        assert "h2h_win_rate" in result.columns
