from langchain_google_genai import ChatGoogleGenerativeAI
from backend.config import settings

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-pro", 
    temperature=0.3,
    google_api_key=settings.GOOGLE_API_KEY
    )

def generate_response(state):

    data_preview = state["query_result"].head(20).to_string()

    prompt = f"""
    User's Question: {state['question']}

    Query Result: {data_preview}

    Explain results in business langauge. Keep response concise and analytical.
    """

    response = llm.invoke(prompt)

    state['answer'] = response.content

    return state
