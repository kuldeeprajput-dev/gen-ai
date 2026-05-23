from fastapi import FastAPI
from ollama import Client
from contextlib import asynccontextmanager
from pydantic import BaseModel

client = Client(
    host="http://localhost:11435"
)

class ChatRequest(BaseModel):
    message: str


@asynccontextmanager
async def lifespan(app: FastAPI):

    client.pull("gemma3:1b")

    yield


app = FastAPI(lifespan=lifespan)


@app.post("/chat")
def chat(body: ChatRequest):

    response = client.chat(
        model="gemma3:1b",
        messages=[
            {
                "role": "user",
                "content": body.message
            }
        ]
    )

    return {
        "response": response["message"]["content"]
    }