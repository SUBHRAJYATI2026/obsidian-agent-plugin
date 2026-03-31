from langgraph.graph import START, END, StateGraph
from src.nodes.reponse import node
from src.states.state import State
from langgraph.graph.state import CompiledStateGraph


def create_graph() -> CompiledStateGraph:
    graph = StateGraph(state_schema=State)
    graph.add_node("agent_node", node)
    graph.add_edge(START, "agent_node")
    graph.add_edge("agent_node", END)
    compiled_graph = graph.compile()
    return compiled_graph
