import pandas as pd

# Fake Data
def predict_game(home_team: str, away_team: str):

    return {
        "home", home_team,
        "away", away_team,
        "home_win_probabilty": 0.52,
        "suggested_bet": "Value on Home" if 0.52 > 0.5 else "No Bet")
    }

