from pydantic import BaseModel, ConfigDict
import pandas as pd
from typing import List


class ParseResult(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    team_name: str
    categories: List[str]
    data: pd.DataFrame

    @property
    def total_games(self) -> int:
        return len(self.data)

    def get_team_record(self):
        """Calculates W-L-OTL directly from the dataframe."""
        # Use vectorized pandas logic instead of loops
        wins = len(self.data[self.data["result"].str.startswith("W", na=False)])
        losses = len(self.data[self.data["result"].str.startswith("L", na=False)])
        return {"wins": wins, "losses": losses}

    def get_wins(self) -> int:
        """Vectorized calculation of wins - much faster than Record.py loops."""
        return len(self.data[self.data["result"].str.startswith("W", na=False)])

    def get_goals_for(self) -> int:
        return self.data["gf"].astype(int).sum()
