def map_hockey_stats(stat):
    short_to_long_mapping = {
        "GP": "Games Played",
        "Date": "Date of the game",
        "Location": "Game Location",
        "Opponent": "Opposing Team",
        "GF": "Goals For",
        "GA": "Goals Against",
        "Result": "Game Result",
        "OverTime": "Overtime Result",
        "Unnamed: 8": "Unnamed Column 8",
        "S": "Shots",
        "PIM": "Penalty Minutes",
        "PPG": "Power Play Goals",
        "PPO": "Power Play Opportunities",
        "SHG": "Short Handed Goals",
        "CF": "Corsi For",
        "CA": "Corsi Against",
        "CF%": "Corsi For Percentage",
        "FF": "Fenwick For",
        "FA": "Fenwick Against",
        "FF%": "Fenwick For Percentage",
        "FOW": "Faceoffs Won",
        "FOL": "Faceoffs Lost",
        "FO%": "Faceoff Win Percentage",
        "oZS%": "Offensive Zone Start Percentage",
        "PDO": "Percentage of Points Earned Out Of Possible Points",
        "team": "Team Name",
        "Home": "Home Team",
        "Visitor": "Visiting Team",
        "HG": "Home Goals",
        "AG": "Away Goals",
    }

    long_to_short_mapping = {v: k for k, v in short_to_long_mapping.items()}

    if stat in short_to_long_mapping:
        return short_to_long_mapping[stat]

    if stat in long_to_short_mapping:
        return long_to_short_mapping[stat]

    return None
