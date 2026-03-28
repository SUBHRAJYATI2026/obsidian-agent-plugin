from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

db_store: dict[int, str] = {}
counter: int = 0

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Item(BaseModel):
    """Schema for the prompt to the ai agent."""

    prompt: str


@app.post("/generate")
def generate(request: Item):
    global counter
    counter += 1
    db_store[counter] = request.prompt
    return {"response": f"Prompt received: {request.prompt}"}


@app.get("/prompts")
def get_prompts():
    return db_store
