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
            idx = title.find(" Game Log")
            return title[0:idx].strip() if idx >= 0 else title.strip()
        return "Unknown"

    def parse_categories(self, soup: BeautifulSoup) -> List[str]:
        table = soup.find("table")
        if isinstance(table, Tag):
            rows = table.find_all("tr")
            if len(rows) > 1:
                return [h.text for h in rows[1].find_all("th")]
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
