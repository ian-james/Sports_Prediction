from typing import List


_RESULT_TO_POINTS = {
    "WIN": 2,
    "OT_WIN": 2,
    "OT_LOSS": 1,
    "LOSS": 0,
}


def get_win_lbls() -> List[str]:
    return ["W", "WIN"]


def get_ot_lbls() -> List[str]:
    # Added "OT", "SO", etc.
    # Logic: Does the string contain any mention of extra time?
    return ["OT", "SO", "OVERTIME", "SHOOTOUT", "OTL", "SOL"]


def get_loss_lbls() -> List[str]:
    return ["L", "LOSS"]


def standardize_result(raw_val: str) -> str:
    if not raw_val:
        return "LOSS"

    val = str(raw_val).upper().strip()

    # The Logic check:
    # Ensure "W" matches "W (OT)" and "W-SO"
    is_win = any(lbl in val for lbl in get_win_lbls())  # ["W", "WIN"]
    is_loss = any(lbl in val for lbl in get_loss_lbls())  # ["L", "LOSS"]
    is_ot = any(lbl in val for lbl in get_ot_lbls())  # ["OT", "SO", etc]

    if is_win:
        return "OT_WIN" if is_ot else "WIN"
    if is_loss:
        return "OT_LOSS" if is_ot else "LOSS"

    return "LOSS"


def get_score_value(raw_val: str) -> int:
    # Use .get() with a default of 0 to prevent KeyError on weird strings
    return _RESULT_TO_POINTS.get(standardize_result(raw_val), 0)
