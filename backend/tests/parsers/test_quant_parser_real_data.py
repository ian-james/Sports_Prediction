from pathlib import Path

import pytest
from bs4 import BeautifulSoup

from src.helpers.file_helpers import load_read_file
from src.parsers.QuantHockeyParser import QuantHockeyParser


@pytest.fixture
def load_quant_html():
    current_dir = Path(__file__).parent

    path = current_dir / ".." / "fixtures" / "Quant_Pens_2025-26.html"

    absolute_path = path.resolve()
    return load_read_file(absolute_path)


class TestQuantHockeyParserWithRealData:
    def test_quant_hockey_pitsburgh_html(self, load_quant_html):
        parser = QuantHockeyParser()
        soup = BeautifulSoup(load_quant_html, "html.parser")

        team_name = parser.parse_team_name(soup)
        categories = parser.parse_categories(soup)

        df = parser.parse_dataframe(soup, team_name, categories)

        # Assert
        print(f"\nParsed Team: {team_name}")
        print(f"Categories: {categories}")
        print(f"DataFrame Shape: {df.shape}")

        # Assertions to verify the real data loaded
        assert team_name == "Pittsburgh Penguins"
        assert not df.empty
        assert "Opponent" in categories
