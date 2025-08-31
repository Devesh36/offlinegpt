from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import requests

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/chat")
async def chat(request: Request):
    data = await request.json()
    user_message = data.get("message", "")
    try:
        response = requests.post(
            "http://localhost:8080/completion",
            json={
                "prompt": user_message,
                "n_predict": 128
            }
        )
        reply = response.json().get("content", "")
        return {"reply": reply}
    except Exception as e:
        print("Error contacting llama.cpp server:", e)
        return {"reply": "Error contacting llama.cpp server."}