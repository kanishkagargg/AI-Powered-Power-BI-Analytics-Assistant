from langchain_google_genai import ChatGoogleGenerativeAI

llm = ChatGoogleGenerativeAI(model='gemini-2.5-flash')

def summarize_chat(state):

    prompt = f"""
    Existing Summary:

    {state['summary']}

    User Question:

    {state['question']}

    Assistant Answer:

    {state['answer']}

    Update summary.

    Keep under 300 words.
    """

    response = llm.invoke(prompt)

    state["summary"] = response.content

    return state 