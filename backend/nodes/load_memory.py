from backend.memory import load_chat

def load_memory_node(state):

    chat = load_chat(state["chat_id"])

    state["summary"] = chat['summary']
    state["title"] = chat['title']

    return state