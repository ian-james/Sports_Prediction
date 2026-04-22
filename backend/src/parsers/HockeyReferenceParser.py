import re
import logging
from typing import List
import pandas as pd
from bs4 import BeautifulSoup, Tag

from .MappingService import MappingService

# Use relative imports to avoid 'module not found'
from .BaseParser import BaseParser

logger = logging.getLogger(__name__)


def build_hockey_reference_url(year: int, team_abbr: str) -> str:
    return f"https://www.hockey-reference.com/teams/{team_abbr}/{year}_gamelog.html"


class HockeyReferenceParser(BaseParser):
    @property
    def name(self) -> str:
        return "HockeyReference"

    def parse_team_name(self, soup: BeautifulSoup) -> str:
        if not soup.title:
            return "Unknown Team"
        title = soup.title.text
        idx = title.find(" Team ")
        if idx >= 0:
            title = title[0:idx]
            title = re.sub(r"^[^A-Z]*", "", title)
        return title.strip()

    def parse_categories(self, soup: BeautifulSoup) -> List[str]:
        table = soup.find("table")
        if not isinstance(table, Tag):
            return []

        rows = table.find_all("tr")
        if len(rows) < 2:
            return []

        headers = [h.text.strip() for h in rows[1].find_all("th")]

        # Manual header fix for HockeyRef's shorthand columns
        if len(headers) > 7:
            headers[2] = "Location"
            headers[6] = "Result"
            headers[7] = "OverTime"
        return headers

    def parse_dataframe(
        self, soup: BeautifulSoup, team_name: str, categories: List[str]
    ) -> pd.DataFrame:
        """Matches BaseParser signature exactly to fix [override] error."""
        table = soup.find("table")
        if not isinstance(table, Tag):
            return pd.DataFrame()

        rows = table.find_all("tr")[2:]
        games = []

        for row in rows:
            # Check for data cells first to avoid header/spacer rows
            td_cells = row.find_all("td")
            if not td_cells:
                continue

            th_cells = row.find_all("th")
            row_data = [c.text.strip() for c in th_cells + td_cells]

            if len(row_data) == len(categories):
                games.append(dict(zip(categories, row_data)))

        df = pd.DataFrame(games)
        if not df.empty:
            df = self.add_derived_columns(df, team_name)
        return df

    def add_derived_columns(self, df: pd.DataFrame, team_name: str) -> pd.DataFrame:
        """Vectorized logic to avoid 'Item str has no attribute where' errors."""
        # Determine location
        is_away = df["Location"] == "@"

        # Home/Away Teams
        df["home_team"] = df["Opponent"].where(is_away, team_name)
        df["away_team"] = df["Opponent"].where(~is_away, team_name)

        # Home/Away Goals
        # Convert to numeric to ensure math works, errors='coerce' handles empty strings
        gf = pd.to_numeric(df["GF"], errors="coerce")
        ga = pd.to_numeric(df["GA"], errors="coerce")

        df["home_goals"] = ga.where(is_away, gf)
        df["away_goals"] = gf.where(is_away, ga)

        # OT Status
        df["ot_status"] = df["OverTime"].apply(
            lambda x: "OT" if any(s in str(x) for s in ["OT", "SO"]) else "REG"
        )

        return df

    def clean_data(self, df: pd.DataFrame, team_name: str) -> pd.DataFrame:
        """Standardizes headers and runs base cleaning."""
        # Fix the [attr-defined] error by using the correct MappingService method
        rename_map = MappingService.standardize_columns(df.columns.tolist())
        df = df.rename(columns=rename_map)

        # Call super().clean_data for dropna and team assignment
        return super().clean_data(df, team_name)
