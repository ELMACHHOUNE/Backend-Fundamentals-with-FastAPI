from fastapi import APIRouter, HTTPException
from app.models import ChatRequest, ChatResponse

router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("", response_model=ChatResponse)
async def chat(request: ChatRequest) -> ChatResponse:
    if not request.message.strip():
        raise HTTPException(status_code=400, detail="Message cannot be empty")
    
    answer = f"Echo: {request.message}"
    return ChatResponse(answer=answer)