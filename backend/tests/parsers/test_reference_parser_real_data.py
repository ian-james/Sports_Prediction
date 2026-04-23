from pathlib import Path

import pytest
from bs4 import BeautifulSoup

from src.helpers.file_helpers import load_read_file
from src.parsers.HockeyReferenceParser import HockeyReferenceParser


@pytest.fixture
def load_reference_html():
    # Use Path(__file__) to ensure we are relative to this test file
    current_dir = Path(__file__).parent
    # Ensure this filename matches the file in your fixtures folder exactly
    path = (current_dir / ".." / "fixtures" / "hockey_reference_example.html").resolve()

    if not path.exists():
        pytest.fail(f"Fixture file missing at: {path}")

    content = load_read_file(path)
    if not content:
        pytest.fail(f"File found but content is empty: {path}")

    return content


class TestHockeyParserWithRealData:  # Renamed for consistency
    def test_reference_hockey_pittsburgh_html(self, load_reference_html):
        parser = HockeyReferenceParser()
        # load_reference_html is already the string content!
        soup = BeautifulSoup(load_reference_html, "html.parser")

        # Do not call load_reference_html() here.
        # If you want to see the HTML, just print the variable:
        # print(load_reference_html[:500])

        team_name = parser.parse_team_name(soup)
        categories = parser.parse_categories(soup)
        df = parser.parse_dataframe(soup, team_name, categories)

        # Assertions
        print(f"\nParsed Team: {team_name}")
        print(f"Categories: {categories}")
        print(f"DataFrame Shape: {df.shape}")

        assert team_name == "Pittsburgh Penguins"
        assert not df.empty
        assert "Opponent" in categories
