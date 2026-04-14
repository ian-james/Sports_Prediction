from fastapi import FASTAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {'status": "Sports Prediction API Running"}
