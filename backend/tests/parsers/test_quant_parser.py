import pytest
from bs4 import BeautifulSoup
from src.parsers.QuantHockeyParser import QuantHockeyParser


@pytest.fixture
def quant_pittsburgh_html():
    """Matches the 'qh-table' and 'qh-th' classes in your QuantHockey file."""
    return """
    <html>
        <head><title>Pittsburgh Penguins Game Log @ NHL 2025-2026</title></head>
        <body>
            <table class="qh-table">
                <thead>
                    <tr>
                        <th class="qh-th">Rk</th>
                        <th class="qh-th">Date</th>
                        <th class="qh-th">Loc</th>
                        <th class="qh-th">Opponent</th>
                        <th class="qh-th">GF</th>
                        <th class="qh-th">GA</th>
                    </tr>
                </thead>
                <tbody>
                    <tr><td>1</td><td>2025-10-07</td><td>Away</td><td>NY Rangers</td><td>3</td><td>0</td></tr>
                </tbody>
            </table>
        </body>
    </html>
    """


class TestQuantParsersWithFakeStructures:
    def test_quant_hockey_pittsburgh(self, quant_pittsburgh_html):
        parser = QuantHockeyParser()
        soup = BeautifulSoup(quant_pittsburgh_html, "lxml")

        # Verify title cleaning logic matches the pattern in your Quant file
        assert parser.parse_team_name(soup) == "Pittsburgh Penguins"

        # Verify it finds the 'qh-table' headers
        categories = parser.parse_categories(soup)

        assert "Loc" in categories
        assert "Opponent" in categories
