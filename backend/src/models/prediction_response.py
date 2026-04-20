from pydantic import BaseModel

class PredictionResponse(BaseModel):
    home_team: str
    away_team: str
    predicted_winner: str
    confidence: float
