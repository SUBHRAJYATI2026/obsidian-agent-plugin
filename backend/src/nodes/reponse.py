from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from pydantic import SecretStr
from src.states.state import State


load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")


def node(state: State) -> State | None:
    model = ChatGroq(
        model="openai/gpt-oss-120b",
        api_key=SecretStr(GROQ_API_KEY) if GROQ_API_KEY else None,
    )
    result = model.invoke([state["prompt"]]).content
    return State(prompt=str(result) if result else "")
