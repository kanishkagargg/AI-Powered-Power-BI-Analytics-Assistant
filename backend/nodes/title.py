from langchain_google_genai import ChatGoogleGenerativeAI

llm = ChatGoogleGenerativeAI(model='gemini-2.5-flash')

def generate_title(state):

    prompt = f"""
    Generate a concise and descriptive title for a chat based on the following summary of the conversation.:

    {state['summary']}

    User Question:

    {state['question']}

    Assistant Answer:

    {state['answer']}

    Generate Title.

    Keep under 10 words.
    """

    response = llm.invoke(prompt)

    state["title"] = response.content

    return state 