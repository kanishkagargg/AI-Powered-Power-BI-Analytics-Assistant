import json
import os

CHAT_DIR = 'backend/chat_store'

os.makedirs(CHAT_DIR, exist_ok=True)

def load_chat(chat_id):

    file_path = f"{CHAT_DIR}/{chat_id}.json"

    if not os.path.exists(file_path):
        return {
            "summary": "",
            "title": "",
            "messages": []
        }

    with open(file_path, 'r') as f:
        return json.load(f)
    

def save_chat(chat_id, data):

    file_path = f"{CHAT_DIR}/{chat_id}.json"

    with open(file_path, 'w') as f:
        json.dump(data, f, indent=4)
