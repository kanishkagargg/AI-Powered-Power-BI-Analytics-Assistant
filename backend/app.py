from fastapi import FastAPI
from pydantic import BaseModel
from backend.memory import load_chat

from backend.graph import graph

app = FastAPI()

class UserQuestion(BaseModel):
    question: str
    chat_id: str

@app.post("/chat") 

def chat(payload: UserQuestion):

    result = graph.invoke({

        "chat_id": payload.chat_id,

        "question": payload.question
    })

    return {

        "answer": result["answer"],

        "sql_query": result["sql_query"],

        "query_result": result["query_result"].to_dict(orient='records')
    }

@app.get("/chat/{chat_id}")

def get_chat(chat_id: str):

    return load_chat(chat_id)

# uvicorn backend.app:app --reload