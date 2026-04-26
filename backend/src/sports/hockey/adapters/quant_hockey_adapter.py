import pandas as pd

from src.sports.hockey.adapters.base_league_adapter import BaseLeagueAdapter
from src.sports.hockey.mappings.league_scoring_mappings import (
    standardize_result,
    _RESULT_TO_POINTS,
)
from src.sports.hockey.mappings.standardized_names import InternalStat


class QuantHockeyAdapter(BaseLeagueAdapter):
    @property
    def raw_to_internal_map(self):
        """Complete mapping for all 27 identified fields."""
        return {
            "Rk": InternalStat.RANK,
            "Date": InternalStat.DATE,
            "Opponent": InternalStat.OPPONENT,
            "Loc": InternalStat.LOCATION,
            "Result": InternalStat.RESULT,
            "GF": InternalStat.GOALS_FOR,
            "GA": InternalStat.GOALS_AGAINST,
            "GD": InternalStat.GOAL_DIFF,
            "PDO": InternalStat.PDO,
            "PDO-A": InternalStat.PDO_ADJ,
            "SF": InternalStat.SHOTS_FOR,
            "SA": InternalStat.SHOTS_AGAINST,
            "SD": InternalStat.SHOT_DIFF,
            "SH%": InternalStat.SH_PCT,
            "SH%-A": InternalStat.SH_PCT_ADJ,
            "FOW": InternalStat.FOW,
            "FOL": InternalStat.FOL,
            "FOD": InternalStat.FO_DIFF,
            "FO%": InternalStat.FO_PCT,
            "SV%": InternalStat.SV_PCT,
            "SV%-A": InternalStat.SV_PCT_ADJ,
            "HITS": InternalStat.HITS,
            "HITS-A": InternalStat.HITS_AGAINST,
            "HITS-D": InternalStat.HIT_DIFF,
            "BS": InternalStat.BLOCKS,
            "BS-A": InternalStat.BLOCKS_AGAINST,
            "BS-D": InternalStat.BLOCK_DIFF,
        }

    @property
    def presentation_order(self):
        """Ensures the final DataFrame is ordered logically for analysis."""
        return [
            InternalStat.RANK,
            InternalStat.DATE,
            InternalStat.OPPONENT,
            InternalStat.IS_HOME,
            InternalStat.RESULT,
            InternalStat.WON,
            InternalStat.OT_GAME,
            InternalStat.POINTS_EARNED,
            InternalStat.GOALS_FOR,
            InternalStat.GOALS_AGAINST,
            InternalStat.GOAL_DIFF,
            InternalStat.SHOTS_FOR,
            InternalStat.SHOTS_AGAINST,
            InternalStat.HITS,
            InternalStat.HITS_AGAINST,
            InternalStat.BLOCKS,
            InternalStat.BLOCKS_AGAINST,
        ]

    def add_derived_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df.copy()

        # 1. Identify the 'Home/Away' column
        # Hockey-Reference tables often leave this unnamed, resulting in 'Unnamed: 4'
        loc_options = ["Location", "Unnamed: 4", "Loc"]
        loc_col = next((c for c in loc_options if c in df.columns), None)

        if loc_col:
            # If it contains '@', it's Away (False). Otherwise, it's Home (True).
            df[InternalStat.IS_HOME.value] = df[loc_col].fillna("") != "@"
        else:
            # Safety fallback: Always create the column to prevent KeyError in tests
            df[InternalStat.IS_HOME.value] = True

        # 2. Derive results (this part is working based on your logs!)
        result_col = InternalStat.RESULT.value
        if result_col in df.columns:
            standard_keys = df[result_col].fillna("").apply(standardize_result)

            df[InternalStat.WON.value] = standard_keys.str.contains("WIN")
            df[InternalStat.OT_GAME.value] = standard_keys.str.contains("OT")
            df[InternalStat.POINTS_EARNED.value] = (
                standard_keys.map(_RESULT_TO_POINTS).fillna(0).astype(int)
            )

        return df
