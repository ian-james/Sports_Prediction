from typing import List
import pandas as pd
from bs4 import BeautifulSoup, Tag
from .base_parser import BaseParser


class QuantHockeyParser(BaseParser):
    @property
    def name(self) -> str:
        return "QuantParser"

    def parse_team_name(self, soup: BeautifulSoup) -> str:
        title_tag = soup.title
        if title_tag:
            title = title_tag.text
            if " Game Log" in title:
                return title.split(" Game Log")[0].strip()
            return title.strip()
        return "Unknown"

    def parse_categories(self, soup: BeautifulSoup) -> List[str]:
        table = soup.find("table", class_="qh-table") or soup.find("table")
        if not isinstance(table, Tag):
            return []

        thead = table.find("thead")
        if isinstance(thead, Tag):
            # QuantHockey uses a multi-row header (hierarchical).
            # The last row [tr] contains the actual column names (Rk, Date, etc.)
            header_rows = thead.find_all("tr")
            if header_rows:
                target_row = header_rows[-1]
                return [th.text.strip() for th in target_row.find_all("th")]
        return []

    def parse_dataframe(
        self, soup: BeautifulSoup, team_name: str, categories: List[str]
    ) -> pd.DataFrame:
        table = soup.find("table", class_="qh-table") or soup.find("table")
        if not isinstance(table, Tag):
            return pd.DataFrame()

        # Using tbody ensures we skip all header rows automatically
        tbody = table.find("tbody")
        rows = tbody.find_all("tr") if isinstance(tbody, Tag) else table.find_all("tr")

        data = []
        for row in rows:
            # Quant uses <th> for index/date/opponent and <td> for stats
            cells = [c.text.strip() for c in row.find_all(["th", "td"])]

            # Now cells and categories will both have the same length (approx 27)
            if len(cells) == len(categories):
                data.append(dict(zip(categories, cells)))

        df = pd.DataFrame(data)
        if not df.empty:
            df = self.add_derived_columns(df, team_name)
        return df

    def add_derived_columns(self, df: pd.DataFrame, team_name: str) -> pd.DataFrame:
        # Standardize Location
        if "Loc." in df.columns:
            df["Location"] = df["Loc."].apply(lambda x: "@" if x == "Away" else "")

        # Extract OverTime status from the Result column (e.g., 'OTW', 'SOL')
        if "Result" in df.columns:
            df["OverTime"] = df["Result"].apply(
                lambda x: "OT" if any(s in str(x) for s in ["OT", "SO"]) else ""
            )
            df["ot_status"] = df["OverTime"].apply(
                lambda x: "OT" if x == "OT" else "REG"
            )

        # Standardize Home/Away teams
        if "Location" in df.columns and "Opponent" in df.columns:
            is_away = df["Location"] == "@"
            df["home_team"] = df["Opponent"].where(is_away, team_name)
            df["away_team"] = df["Opponent"].where(~is_away, team_name)

        return df
