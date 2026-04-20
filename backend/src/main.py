from fastapi import FastAPI
from src.routers.prediction_routes import router as prediction_router

app = FastAPI()

# Routes
app.include_router(prediction_router)

@app.get("/")
def read_root():
    return {"status": "Sports Prediction API Running"}