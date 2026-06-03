from langgraph.graph import StateGraph

from backend.state import ChatState

from backend.nodes.load_memory import load_memory_node
from backend.nodes.retrieve_context import retrieve_context
from backend.nodes.generate_sql import generate_sql 
from backend.nodes.run_query import run_query
from backend.nodes.generate_response import generate_response
from backend.nodes.summarize_chat import summarize_chat
from backend.nodes.save_memory import save_memory_node
from backend.nodes.title import generate_title

def title_router(state):

    if state.get("title"):

        return "save_memory"

    if len(
        state.get(
            "messages",
            []
        )
    ) > 0:

        return "save_memory"

    return "generate_title"


graph = StateGraph(ChatState)

graph.add_node("load_memory", load_memory_node)
graph.add_node("retrieve_context", retrieve_context)
graph.add_node("generate_sql", generate_sql)
graph.add_node("run_query", run_query)
graph.add_node("generate_response", generate_response)
graph.add_node("summarize_chat", summarize_chat)
graph.add_node("save_memory", save_memory_node)
graph.add_node("generate_title", generate_title)

graph.set_entry_point("load_memory")
graph.add_edge("load_memory", "retrieve_context")
graph.add_edge("retrieve_context", "generate_sql")
graph.add_edge("generate_sql", "run_query")
graph.add_edge("run_query", "generate_response")
graph.add_edge("generate_response", "summarize_chat")
graph.add_conditional_edges(
    "summarize_chat",
    title_router, {
        "generate_title":"generate_title",
        "save_memory":"save_memory"
    }
)
graph.add_edge("generate_title", "save_memory")

graph = graph.compile()