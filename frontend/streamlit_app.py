import streamlit as st
import requests
import uuid
import os
import json
import numpy as np

# ----------------------------------
# CONFIG
# ----------------------------------

API_URL = "http://127.0.0.1:8000"

CHAT_DIR = "backend/chat_store"

# ----------------------------------
# PAGE CONFIG
# ----------------------------------

st.set_page_config(
    page_title="PowerBI Copilot",
    layout="wide"
)

st.title("Chatbot for your PowerBI Dashboard")

# ----------------------------------
# HELPERS
# ----------------------------------

def get_chat_list():

    chats = []

    for file in os.listdir(CHAT_DIR):

        if file.endswith(".json"):

            chat_id = file.replace(
                ".json",
                ""
            )

            with open(
                os.path.join(CHAT_DIR, file),
                "r"
            ) as f:

                data = json.load(f)

            if len(data["messages"]) > 0:

                title = f"{data['title']}..."

            else:

                title = "New Chat"

            chats.append(
                {
                    "id": chat_id,
                    "title": title
                }
            )

    return chats


def load_chat(chat_id):

    try:

        response = requests.get(
            f"{API_URL}/chat/{chat_id}"
        )

        if response.status_code == 200:

            return response.json()

    except:

        pass

    return {
        "summary": "",
        "messages": []
    }

# ----------------------------------
# SESSION STATE
# ----------------------------------

if "is_new_chat" not in st.session_state:

    st.session_state.is_new_chat = False

if "chat_id" not in st.session_state:

    st.session_state.chat_id = str(
        uuid.uuid4()
    )

# ----------------------------------
# SIDEBAR
# ----------------------------------

st.sidebar.title("Chats")

if st.sidebar.button(
    "➕ New Chat",
    use_container_width=True
):

    st.session_state.chat_id = str(
        uuid.uuid4()
    )

    st.session_state.is_new_chat = True


    st.rerun()

# ----------------------------------
# EXISTING CHATS
# ----------------------------------

chat_list = get_chat_list()

chat_titles = {

    chat["title"]: chat["id"]

    for chat in chat_list
}

if len(chat_list) > 0:

    # selected_chat = st.sidebar.radio(

    #     "Previous Chats",

    #     chat_list,

    #     index=0

    # )

    selected_title = st.sidebar.radio(

    "Previous Chats",

    list(chat_titles.keys())

    )

    selected_chat = chat_titles[
        selected_title
    ]

    if not st.session_state.is_new_chat:

        if selected_chat != st.session_state.chat_id:

            st.session_state.chat_id = selected_chat

            st.rerun()

# ----------------------------------
# LOAD CURRENT CHAT
# ----------------------------------

chat_data = load_chat(
    st.session_state.chat_id
)

# ----------------------------------
# SHOW CHAT HISTORY
# ----------------------------------

for msg in chat_data.get(
    "messages",
    []
):

    with st.chat_message("user"):

        st.write(
            msg["question"]
        )

    with st.chat_message("assistant"):

        st.write(
            msg["assistant"]
        )

        if "sql_query" in msg:

            with st.expander(
                "Generated SQL"
            ):

                st.code(
                    msg["sql_query"],
                    language="sql"
                )

        if "query_result" in msg:

            with st.expander(
                "Query Result"
            ):

                st.dataframe(
                    msg["query_result"]
                )

# ----------------------------------
# QUESTION INPUT
# ----------------------------------

question = st.chat_input(
    "Ask about your Power BI dashboard..."
)

# ----------------------------------
# SEND QUESTION
# ----------------------------------

if question:

    with st.chat_message("user"):

        st.write(question)

    payload = {

        "question": question,

        "chat_id": st.session_state.chat_id
    }

    response = requests.post(

        f"{API_URL}/chat",

        json=payload

    )

    if response.status_code == 200:

        result = response.json()

        with st.chat_message("assistant"):

            st.write(
                result["answer"]
            )

            if "query_result" in result:

                with st.expander(
                    "Query Result"
                ):

                    st.dataframe(
                        result["query_result"]
                    )

            if "sql_query" in result:

                with st.expander(
                    "Generated SQL"
                ):

                    st.code(
                        result["sql_query"],
                        language="sql"
                    )

        st.rerun()

    else:

        st.error(
            "Failed to get response."
        )

# streamlit run frontend/streamlit_app.py        