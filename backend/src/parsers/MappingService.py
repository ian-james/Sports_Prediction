from typing import Dict, List


class MappingService:
    """Unified source of truth for NHL team abbreviations and statistic nomenclature."""

    _TEAM_MAP: Dict[str, str] = {
        "ANA": "Anaheim Ducks",
        "ARI": "Arizona Coyotes",
        "PHX": "Arizona Coyotes",
        "BOS": "Boston Bruins",
        "BUF": "Buffalo Sabres",
        "CGY": "Calgary Flames",
        "CAR": "Carolina Hurricanes",
        "CHI": "Chicago Blackhawks",
        "CBJ": "Columbus Blue Jackets",
        "COL": "Colorado Avalanche",
        "DAL": "Dallas Stars",
        "DET": "Detroit Red Wings",
        "EDM": "Edmonton Oilers",
        "FLA": "Florida Panthers",
        "LAK": "Los Angeles Kings",
        "MIN": "Minnesota Wild",
        "MTL": "Montreal Canadiens",
        "NJD": "New Jersey Devils",
        "NSH": "Nashville Predators",
        "NYI": "New York Islanders",
        "NYR": "New York Rangers",
        "OTT": "Ottawa Senators",
        "PHI": "Philadelphia Flyers",
        "PIT": "Pittsburgh Penguins",
        "SEA": "Seattle Kraken",
        "SJS": "San Jose Sharks",
        "STL": "St. Louis Blues",
        "TBL": "Tampa Bay Lightning",
        "TOR": "Toronto Maple Leafs",
        "UTA": "Utah Hockey Club",
        "VAN": "Vancouver Canucks",
        "VEG": "Vegas Golden Knights",
        "WSH": "Washington Capitals",
        "WPG": "Winnipeg Jets",
    }

    _RAW_TO_INTERNAL: Dict[str, str] = {
        "Date": "date",
        "Result": "result",
        "GF": "goals_for",
        "GA": "goals_against",
        "GD": "goal_differential",
        "GP": "games_played",
        "Rk": "rank",
        "Loc": "location",
        "Location": "location",
        "Opponent": "opponent",
        "OverTime": "overtime_status",
        "S": "shots",
        "PIM": "penalty_minutes",
        "PPG": "power_play_goals",
        "PPO": "power_play_opportunities",
        "SHG": "short_handed_goals",
        "CF%": "corsi_for_percentage",
        "SV%": "save_percentage",
        "SH%": "shooting_percentage",
        "BS": "blocked_shots",
        "HITS": "hits",
    }

    @classmethod
    def get_full_team_name(cls, abbreviation: str) -> str:
        return cls._TEAM_MAP.get(abbreviation.upper(), abbreviation)

    @classmethod
    def standardize_columns(cls, raw_columns: List[str]) -> Dict[str, str]:
        """Maps site-specific headers to internal snake_case names."""
        return {
            col: cls._RAW_TO_INTERNAL.get(col, col.lower().replace(" ", "_"))
            for col in raw_columns
        }
