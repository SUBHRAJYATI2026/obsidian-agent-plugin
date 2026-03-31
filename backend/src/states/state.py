from typing import TypedDict
from pydantic import SecretStr

class State(TypedDict):
    """State of the graph"""

    prompt: str
