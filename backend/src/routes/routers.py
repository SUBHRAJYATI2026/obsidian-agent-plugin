from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from src.graph import create_graph
from src.states.state import State

router = APIRouter()
graph = create_graph()

db_store: dict[int, dict[str, str]] = {}
counter: int = 0


@router.post("/generate")
def generate(request: str):
    global counter
    result = graph.invoke({"prompt": request})
    counter += 1
    db_store[counter] = {"prompt": request, "response": result["prompt"]}
    return {"prompt": request, "response": result["prompt"]}


@router.get("/prompts")
def get_prompts():
    return db_store
