import pytest
from bs4 import BeautifulSoup
from src.parsers.HockeyReferenceParser import HockeyReferenceParser


@pytest.fixture
def hr_pittsburgh_html():
    return """
    <div id="all_games">
        <table id="games">
            <thead>
                <tr>
                    <th data-stat="games">GP</th>
                    <th data-stat="date_game">Date</th>
                    <th data-stat="game_location"></th>
                    <th data-stat="opp_name">Opponent</th>
                    <th data-stat="goals">GF</th>
                    <th data-stat="opp_goals">GA</th>
                    <th data-stat="overtimes">OverTime</th>
                </tr>
            </thead>
            <tbody>
                <tr data-row="0">
                    <th scope="row">1</th>
                    <td data-stat="date_game">2025-10-07</td>
                    <td data-stat="game_location">@</td>
                    <td data-stat="opp_name">New York Rangers</td>
                    <td data-stat="goals">3</td>
                    <td data-stat="opp_goals">0</td>
                    <td data-stat="overtime">OT</td>
                </tr>
            </tbody>
        </table>
    </div>
    """


class TestParsersWithRealStructures:
    def test_hockey_reference_pittsburgh(self, hr_pittsburgh_html):
        parser = HockeyReferenceParser()
        soup = BeautifulSoup(hr_pittsburgh_html, "lxml")

        # Verify it looks for the 'games' table and extracts headers correctly
        categories = parser.parse_categories(soup)
        print(categories)

        # We check for 'Opponent' specifically as it failed in your previous run
        assert "Opponent" in categories
        assert "GF" in categories

        df = parser.parse_dataframe(soup, "Pittsburgh Penguins", categories)
        assert not df.empty
        assert df.iloc[0]["Opponent"] == "New York Rangers"
