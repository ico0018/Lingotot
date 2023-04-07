import asyncio
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Message(BaseModel):
    content: str

@app.post("/send-message/")
async def send_message(message: Message):
    await asyncio.sleep(10)
    return {"status": "success", "message": message.content[:5]}
