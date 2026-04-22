import logging
import httpx
import pandas as pd
from bs4 import BeautifulSoup
from abc import ABC, abstractmethod
from typing import List

logger = logging.getLogger(__name__)


class BaseParser(ABC):
    def __init__(self, timeout: float = 10.0):
        self.client = httpx.Client(timeout=timeout, follow_redirects=True)

    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @abstractmethod
    def parse_team_name(self, soup: BeautifulSoup) -> str:
        pass

    @abstractmethod
    def parse_categories(self, soup: BeautifulSoup) -> List[str]:
        pass

    @abstractmethod
    def parse_dataframe(
        self, soup: BeautifulSoup, team_name: str, categories: List[str]
    ) -> pd.DataFrame:
        pass

    def clean_data(self, df: pd.DataFrame, team_name: str) -> pd.DataFrame:
        """Shared cleaning logic."""
        df = df.dropna(axis=1, how="all")
        df["team"] = team_name
        return df
