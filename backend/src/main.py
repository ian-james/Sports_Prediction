from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# Move this later
class PredictionResponse(BaseModel):
    home_team: str
    away_team: str
    predicted_winner: str
    confidence: float

def predict_game( home:str, away: str) -> PredictionResponse:
    return PredictionResponse(
            home_team=home,
            away_team=away,
            predicted_winner=home,
            confidence=0.5
            )

@app.get("/predict", response_model=PredictionResponse)
def get_prediction(home: str, away: str) -> PredictionResponse :
    return predict_game(home,away)

@app.get("/predict_fake",response_model=PredictionResponse) 
def get_fake_prediction(home: str, away: str) -> PredictionResponse :
    return predict_game("Toronto","Montreal")

@app.get("/")
def read_root():
    return {"status": "Sports Prediction API Running"}

