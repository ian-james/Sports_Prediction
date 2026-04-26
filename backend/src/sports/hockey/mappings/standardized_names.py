from enum import StrEnum


class InternalStat(StrEnum):
    # Core
    RANK = "rank"
    DATE = "date"
    OPPONENT = "opponent"
    LOCATION = "location"
    RESULT = "result"

    # Scoring & Efficiency
    GOALS_FOR = "goals_for"
    GOALS_AGAINST = "goals_against"
    GOAL_DIFF = "goal_differential"
    PDO = "pdo"
    PDO_ADJ = "pdo_adjusted"

    # Shots
    SHOTS_FOR = "shots_for"
    SHOTS_AGAINST = "shots_against"
    SHOT_DIFF = "shot_differential"
    SH_PCT = "shooting_percentage"
    SH_PCT_ADJ = "shooting_percentage_adjusted"
    SV_PCT = "save_percentage"
    SV_PCT_ADJ = "save_percentage_adjusted"

    # Faceoffs
    FOW = "faceoffs_won"
    FOL = "faceoffs_lost"
    FO_DIFF = "faceoff_differential"
    FO_PCT = "faceoff_percentage"

    # Physical (Hits)
    HITS = "hits"
    HITS_AGAINST = "hits_against"
    HIT_DIFF = "hit_differential"

    # Defensive (Blocks)
    BLOCKS = "blocked_shots"
    BLOCKS_AGAINST = "blocked_shots_against"
    BLOCK_DIFF = "blocked_shot_differential"

    # Record & Standings
    GAMES_PLAYED = "games_played"
    WINS = "wins"
    LOSSES = "losses"
    OT_LOSSES = "ot_losses"  # Includes Shootout Losses
    POINTS = "points"
    POINTS_PCT = "points_percentage"

    # Streaks & Last 10
    STREAK = "streak"
    LAST_10 = "last_10"

    # Goals (Standing Context)
    GOALS_FOR_PER_GAME = "gf_per_game"
    GOALS_AGAINST_PER_GAME = "ga_per_game"

    # Derived / Engineered
    IS_HOME = "is_home"
    WON = "won"
    OT_GAME = "ot_game"
    POINTS_EARNED = "points_earned"

    @property
    def display(self) -> str:
        """Returns the human-readable version of the stat."""
        return _DISPLAY_NAME_MAP.get(self, self.value.replace("_", " ").title())


_DISPLAY_NAME_MAP = {
    InternalStat.DATE: "Date",
    InternalStat.OPPONENT: "Opponent",
    InternalStat.LOCATION: "Venue",
    InternalStat.RESULT: "Outcome",
    InternalStat.GOALS_FOR: "Goals For",
    InternalStat.GOALS_AGAINST: "Goals Against",
    InternalStat.GOAL_DIFF: "Goal Diff",
    InternalStat.PDO: "PDO",
    InternalStat.PDO_ADJ: "Adj. PDO",
    InternalStat.SHOTS_FOR: "Shots For",
    InternalStat.SHOTS_AGAINST: "Shots Against",
    InternalStat.SH_PCT: "Shooting %",
    InternalStat.SV_PCT: "Save %",
    InternalStat.FOW: "Faceoffs Won",
    InternalStat.FOL: "Faceoffs Lost",
    InternalStat.HITS: "Hits",
    InternalStat.HITS_AGAINST: "Opp. Hits",
    InternalStat.BLOCKS: "Blocks",
    InternalStat.BLOCKS_AGAINST: "Opp. Blocks",
    InternalStat.GAMES_PLAYED: "GP",
    InternalStat.WINS: "W",
    InternalStat.LOSSES: "L",
    InternalStat.OT_LOSSES: "OTL",
    InternalStat.POINTS: "Pts",
    InternalStat.POINTS_PCT: "Pts %",
}
