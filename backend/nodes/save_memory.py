from backend.memory import load_chat, save_chat

def save_memory_node(state):

    chat = load_chat(state["chat_id"])

    chat['summary'] = state['summary']

    chat["title"] = state["title"]

    chat["messages"].append({

    "question": state["question"],

    "assistant": state["answer"],

    "sql_query": state["sql_query"],

    "query_result":
        state["query_result"]
            .head(20)
            .to_dict(
                orient="records"
            )
})

    save_chat(state["chat_id"], chat)

    return state