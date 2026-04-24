import pandas as pd

from src.sports.hockey.adapters.base_league_adapter import BaseLeagueAdapter
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
            InternalStat.RESULT,
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
        """Satisfies BaseLeagueAdapter contract. Add custom logic here later."""
        return df
