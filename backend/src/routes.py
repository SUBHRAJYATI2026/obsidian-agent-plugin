from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter()

db_store: dict[int, str] = {}
counter: int = 0


class Item(BaseModel):
    """Schema for the prompt to the ai agent."""

    prompt: str


@router.post("/generate")
def generate(request: Item):
    global counter
    counter += 1
    db_store[counter] = request.prompt
    return {"response": f"Prompt received: {request.prompt}"}


@router.get("/prompts")
def get_prompts():
    return db_store
