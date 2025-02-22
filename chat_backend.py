from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

app = FastAPI()

class MessageRequest(BaseModel):
    incoming_message: str
    chat_history: List[str]

class MessageResponse(BaseModel):
    reply: str

@app.post("/process_message", response_model=MessageResponse)
async def process_message(request: MessageRequest):
    # Replace with your Python logic
    response = f"Processed: {request.incoming_message}"
    return {"reply": response}
