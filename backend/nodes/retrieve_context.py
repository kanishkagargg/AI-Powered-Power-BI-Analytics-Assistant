import json

with open(
    "backend/schema_docs/table.json", "r"
) as f:
    
    docs = json.load(f)

def retrieve_context(state):

    question = state["question"]

    question = question.lower()

    matched_context = []

    keywords = docs.get(
        "keywords", []
    )  

    keyword_match = False

    for keyword in keywords:
        if keyword.lower() in question:
            keyword_match = True
            break

    if keyword_match:

        context = f"""
        DASHBOARD:
        {docs.get('dashboard_name')}

        BASE TABLE:
        {docs.get('base_table')}

        DIMENSIONS:
        {docs.get('dimensions')}

        MEASURES:
        {docs.get('measures')}
        """    
        matched_context.append(context)

    matched_context = "\n\n".join(matched_context)

    state["context"] = matched_context

    return state
