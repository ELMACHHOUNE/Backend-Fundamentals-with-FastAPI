from fastapi import APIRouter, HTTPException
from app.models import SummariseRequest, SummariseResponse

router = APIRouter(prefix="/summarise", tags=["summarise"])


def simple_summarize(text: str, max_bullets: int) -> list[str]:
    sentences = [s.strip() for s in text.split(".") if s.strip()]
    
    if not sentences:
        return ["No content to summarise"]
    
    bullets = []
    for i, sentence in enumerate(sentences):
        if i >= max_bullets:
            break
        bullets.append(sentence + ".")
    
    if not bullets:
        bullets = [text[:200] + "..." if len(text) > 200 else text]
    
    return bullets


@router.post("", response_model=SummariseResponse)
async def summarise(request: SummariseRequest) -> SummariseResponse:
    if not request.text.strip():
        raise HTTPException(status_code=400, detail="Text cannot be empty")
    
    summary_bullets = simple_summarize(request.text, request.max_bullets)
    summary_text = " ".join(summary_bullets)
    
    return SummariseResponse(
        summary=summary_bullets,
        original_length=len(request.text),
        summary_length=len(summary_text)
    )