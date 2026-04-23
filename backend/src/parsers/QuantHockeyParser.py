from typing import List

from bs4 import BeautifulSoup, Tag
import pandas as pd
from .BaseParser import BaseParser


class QuantHockeyParser(BaseParser):
    @property
    def name(self) -> str:
        return "QuantParser"

    def parse_team_name(self, soup: BeautifulSoup) -> str:
        title_tag = soup.title
        if title_tag:
            title = title_tag.text
            # Use a more robust split; QuantHockey titles usually follow
            # "Team Name Game Log @ ..."
            if " Game Log" in title:
                return title.split(" Game Log")[0].strip()
            return title.strip()
        return "Unknown"

    def parse_categories(self, soup: BeautifulSoup) -> List[str]:
        # QuantHockey tables use the class 'qh-table'
        table = soup.find("table", class_="qh-table") or soup.find("table")

        if isinstance(table, Tag):
            # Look for th tags with the specific QuantHockey header class
            headers = table.find_all("th", class_="qh-th")

            # Fallback to standard thead search if classes aren't present
            if not headers:
                thead = table.find("thead")
                if isinstance(thead, Tag):
                    headers = thead.find_all("th")

            if headers:
                return [h.text.strip() for h in headers]

            # Last resort: your original row-based logic
            rows = table.find_all("tr")
            for row in rows[:2]:  # Check first two rows
                cols = row.find_all("th")
                if cols:
                    return [c.text.strip() for c in cols]
        return []

    def parse_dataframe(
        self, soup: BeautifulSoup, team_name: str, categories: List[str]
    ) -> pd.DataFrame:
        table = soup.find("table")
        if not isinstance(table, Tag):
            return pd.DataFrame()

        rows = table.find_all("tr")[2:]
        data = []
        for row in rows:
            cells = [c.text.strip() for c in row.find_all(["th", "td"])]
            if len(cells) == len(categories):
                data.append(dict(zip(categories, cells)))
        return pd.DataFrame(data)
