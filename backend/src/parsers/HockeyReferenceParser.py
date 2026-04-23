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
        # Pattern: "2025-26 Pittsburgh Penguins Schedule | Hockey-Reference.com"
        # Remove the " Schedule | ..." part
        if " Schedule" in title:
            title = title.split(" Schedule")[0]

        # Remove leading years (e.g., 2025-26)
        title = re.sub(r"^\d{4}-\d{2}\s+", "", title)

        return title.strip()

    def parse_categories(self, soup: BeautifulSoup) -> List[str]:
        # HockeyRef usually IDs the main table as 'games'
        table = soup.find("table", id="games") or soup.find("table")

        if not isinstance(table, Tag):
            return []

        # Find headers specifically in the thead to avoid body/row confusion
        thead = table.find("thead")
        if isinstance(thead, Tag):
            # Grab the last row of the header (sometimes there are multi-row headers)
            header_row = thead.find_all("tr")[-1]
            # headers = [h.text.strip() for h in header_row.find_all("th")]

            # Use data-stat attributes for internal reliability if text is empty
            # (e.g. the Location column '@' often has an empty text header)
            final_headers = []
            for h in header_row.find_all("th"):
                text = h.text.strip()
                if not text and h.get("data-stat") == "game_location":
                    final_headers.append("Location")
                else:
                    final_headers.append(text)

            # Apply your manual index fixes if names are still missing
            if len(final_headers) > 7:
                if not final_headers[2]:
                    final_headers[2] = "Location"
                if not final_headers[6]:
                    final_headers[6] = "Result"
                if not final_headers[7]:
                    final_headers[7] = "OverTime"

            return final_headers

        return []

    def parse_dataframe(
        self, soup: BeautifulSoup, team_name: str, categories: List[str]
    ) -> pd.DataFrame:
        # Find the specific games table
        table = soup.find("table", id="games") or soup.find("table")
        if not isinstance(table, Tag):
            return pd.DataFrame()

        # Target the tbody specifically.
        # Real Hockey-Ref and your Test Mock both put data here.
        tbody = table.find("tbody")
        if isinstance(tbody, Tag):
            rows = tbody.find_all("tr")
        else:
            rows = table.find_all("tr")

        games = []
        for row in rows:
            # 1. Skip month header rows (e.g., 'October') which have no 'td' cells
            td_cells = row.find_all("td")
            if not td_cells:
                continue

            # 2. Hockey-Ref puts the rank/GP in a 'th' and stats in 'td'
            th_cells = row.find_all("th")
            row_data = [c.text.strip() for c in th_cells + td_cells]

            # 3. Only append if the data matches our header count
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
