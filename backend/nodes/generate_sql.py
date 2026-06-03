from langchain_google_genai import ChatGoogleGenerativeAI
from backend.config import settings

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-pro", 
    temperature=0, 
    google_api_key=settings.GOOGLE_API_KEY
    )

def generate_sql(state):

    prompt = f"""
    You are a expert assistant that generates SQL queries based on the user's question, provided context and current chat history. 
    The context contains information about the database schema, including table names and their respective columns.

    IMPORTANT RULES:
    - USE only this table in query: "db.csv"
    - NEVER invent table or column names that are not present in the context
    - Return ONLY SQL
    - Do not use "db.csv".age or "db.csv".gender. Instead, use age or region in your SQL query.
    - Use summary if user references previous discussion.

    Chat History: {state['summary']}

    Database Schema Context: {state['context']}

    User Question: {state['question']}
    """

    response = llm.invoke(prompt)

    sql_query = response.content

    sql_query = sql_query.replace("```sql", "").replace("```", "").strip()

    state["sql_query"] = sql_query

    return state