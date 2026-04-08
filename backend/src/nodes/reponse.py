from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from pydantic import SecretStr
from src.states.state import State
from src.templates.prompt_template import prompt_template


load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

prompt = ChatPromptTemplate.from_template(template=prompt_template)


def node(state: State) -> State | None:
    model = ChatGroq(
        model="openai/gpt-oss-120b",
        api_key=SecretStr(GROQ_API_KEY) if GROQ_API_KEY else None,
    )
    prompt_value = prompt.invoke({"prompt": state["prompt"]})
    result = model.invoke(prompt_value).content
    return State(prompt=str(result) if result else "")
