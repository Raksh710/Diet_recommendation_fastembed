import uvicorn
from fastapi import FastAPI
from params import Question
from get_recommendations import recommend

app = FastAPI()

@app.get("/")
def index():
    return {"message": "Testing API Diet Recommendation"}

@app.post("/dietrecommendation")
def recommend_recipe(data: Question):
    resp = recommend(query=data.query, data_path=data.data_path, threshold=data.threshold, n=data.n)
    return resp


if __name__=='__main__':
    try:
        uvicorn.run(app, host="0.0.0.0", port=4000)
    except KeyboardInterrupt:
        print("Server shutdown requested by user (Ctrl+C)")