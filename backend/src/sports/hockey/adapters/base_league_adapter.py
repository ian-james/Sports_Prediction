from abc import ABC, abstractmethod
from typing import Dict, List
import pandas as pd

from src.sports.hockey.mappings.standardized_names import InternalStat


class BaseLeagueAdapter(ABC):
    @property
    @abstractmethod
    def raw_to_internal_map(self) -> Dict[str, InternalStat]:
        """Maps Raw Scraper Headers -> InternalStat Enum."""
        pass

    @property
    @abstractmethod
    def presentation_order(self) -> List[InternalStat]:
        """Defines the final column order for display."""
        pass

    @abstractmethod
    def add_derived_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        """Logic for calculating is_home, points, goal_diff, etc."""
        pass

    def finalize(self, df: pd.DataFrame) -> pd.DataFrame:
        """Standard sorting and cleanup."""
        df = self.add_derived_columns(df)

        # Change GAME_DATE to DATE to match your Enum
        if InternalStat.DATE.value in df.columns:
            df[InternalStat.DATE.value] = pd.to_datetime(df[InternalStat.DATE.value])
            df = df.sort_values(by=InternalStat.DATE.value, ascending=True)

        # Ensure we use .value for column filtering
        existing_cols = [
            c.value for c in self.presentation_order if c.value in df.columns
        ]
        return df[existing_cols]
