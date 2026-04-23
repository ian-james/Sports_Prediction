# The converter can provide the mapping of all the names
# Creates the columns that are required for the dataframe
# Reorders the columns for presentation
# Ensures sorted properly by date.


def get_column_format(column_name):
    short_to_long_mapping = {
        "Rk": "Rank",
        "Date": "Date of the game",
        "Opponent": "Opposing team",
        "Loc": "Location",
        "Result": "Game result",
        "GF": "Goals For",
        "GA": "Goals Against",
        "GD": "Goal Differential",
        "PDO": "Percentage of Points Earned Out Of Possible Points",
        "PDO-A": "Adjusted PDO",
        "SF": "Shots For",
        "SA": "Shots Against",
        "SD": "Shot Differential",
        "SH%": "Shooting Percentage",
        "SH%-A": "Adjusted Shooting Percentage",
        "FOW": "Faceoffs Won",
        "FOL": "Faceoffs Lost",
        "FOD": "Faceoff Differential",
        "FO%": "Faceoff Percentage",
        "SV%": "Save Percentage",
        "SV%-A": "Adjusted Save Percentage",
        "HITS": "Number of Hits",
        "HITS-A": "Opponent's Hits",
        "HITS-D": "Hit Differential",
        "BS": "Blocked Shots",
        "BS-A": "Opponent's Blocked Shots",
        "BS-D": "Blocked Shot Differential",
    }

    if column_name in short_to_long_mapping:
        return short_to_long_mapping[column_name]

    long_to_short_mapping = {v: k for k, v in short_to_long_mapping.items()}

    if column_name in long_to_short_mapping:
        return long_to_short_mapping[column_name]

    return column_name
