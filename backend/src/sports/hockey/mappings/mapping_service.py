import pandas as pd
from src.sports.hockey.mappings.standardized_names import InternalStat
from src.sports.hockey.mappings.team_mappings import _TEAM_MAP
from src.sports.hockey.mappings.league_scoring_mappings import (
    _RESULT_TO_POINTS,
    standardize_result,
)
from src.sports.hockey.adapters.base_league_adapter import BaseLeagueAdapter


class MappingService:
    """Unified source of truth using external adapters and centralized maps."""

    @classmethod
    def get_full_team_name(cls, abbreviation: str) -> str:
        return _TEAM_MAP.get(abbreviation.upper(), abbreviation)

    @classmethod
    def normalize_columns(
        cls, df: pd.DataFrame, adapter: BaseLeagueAdapter
    ) -> pd.DataFrame:
        """Standardizes raw headers into internal snake_case using the adapter."""
        rename_map = {
            raw: stat.value for raw, stat in adapter.raw_to_internal_map.items()
        }
        return df.rename(columns=rename_map)

    @classmethod
    def get_display_columns(cls, df: pd.DataFrame) -> pd.DataFrame:
        """Flips internal snake_case keys back to 'Pretty' print-friendly names."""
        # This relies on the .display property restored in standardized_names.py
        display_map = {stat.value: stat.display for stat in InternalStat}
        return df.rename(columns=display_map)

    @staticmethod
    def get_points_from_result(result_str: str) -> int:
        if not result_str:
            return 0
        standard_key = standardize_result(result_str)
        return _RESULT_TO_POINTS.get(standard_key, 0)
