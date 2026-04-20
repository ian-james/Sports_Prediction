from fastapi import APIRouter
from src.models.prediction_response import PredictionResponse

router = APIRouter(prefix="/predict", tags=["Prediction"])


def predict_game(home: str, away: str) -> PredictionResponse:
    return PredictionResponse(
        home_team=home, away_team=away, predicted_winner=home, confidence=0.5
    )


@router.get("/", response_model=PredictionResponse)
def get_prediction(home: str, away: str) -> PredictionResponse:
    return predict_game(home, away)


@router.get("/_fake", response_model=PredictionResponse)
def get_fake_prediction(home: str, away: str) -> PredictionResponse:
    return predict_game("Toronto", "Montreal")
