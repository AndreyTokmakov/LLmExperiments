from typing import Dict

import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
import requests
from requests import Response

app = FastAPI(title="Ollama DeepSeek API")

OLLAMA_URL: str = "http://localhost:11434/api/generate"


class PromptRequest(BaseModel):
    prompt: str


class PromptResponse(BaseModel):
    response: str


@app.post("/generate", response_model=PromptResponse)
def generate(request: PromptRequest):
    payload = {
        "model": "deepseek-r1:1.5b",
        "prompt": request.prompt,
        "stream": False
    }

    response: Response = requests.post(OLLAMA_URL, json=payload)
    response.raise_for_status()

    data: Dict = response.json()
    return {"response": data["response"]}


if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=52525, log_level="info")
