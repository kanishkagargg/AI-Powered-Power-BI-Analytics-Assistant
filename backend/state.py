from typing import TypedDict

class ChatState(TypedDict):
    chat_id: int
    question: str
    summary: str
    context: str
    sql_query: str
    query_result: str
    answer: str
    title: str