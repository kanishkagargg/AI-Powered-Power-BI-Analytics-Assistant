# PowerBI Chatbot with Dynamic SQL and Memory

## Objective
This project builds a lightweight chat assistant for a PowerBI-style dataset with FastAPI middleware, dynamic SQL generation, and session memory. It is designed to answer analytical questions more precisely than a generic Copilot-style assistant by generating exact SQL, executing it against the local dataset, returning both the result and the query and maintaining conversational context across multiple chat surpassing PowerBI Copilot capabilities.

### Why Not Just Use Copilot?

While dashboard copilots are useful for summarizing visuals and answering common questions, they can be constrained by:

- Existing dashboard measures and dimensions
- Predefined semantic model logic
- Limited conversational memory
- Dataset size limitations
- Reduced transparency into how answers are generated

This project addresses those limitations by: 

- Dynamic SQL-based analysis instead of heuristic dashboard inference
- Well defined schema that explains raw data used + dashboard logic
- Uses actual dataset queries, not just precomputed dashboard calculations
- Returns query text and result evidence for transparency
- Preserves chat history and summary memory across sessions
- Cross-dashboard knowledge (Tentative)

## Demo Use Cases

### 1) Age bracket count by gender
- User asked: `How many females are there within age bracket of 54-60?`
- Copilot answer: `411,067` based on a rigid dashboard range of `54-62`
<img width="700" height="285.7" alt="image (2)" src="https://github.com/user-attachments/assets/e5fbc9d1-657d-4d84-b153-988954b563ef" />


- Our chatbot answer: 
  - `Based on the query, there are **319,826** females in the 54-60 age bracket.`
  - SQL:

```sql
SELECT COUNT(*) FROM "db.csv" WHERE gender = 'Female' AND age BETWEEN 54 AND 60
```

<img width="700" height="285.7" alt="image" src="https://github.com/user-attachments/assets/48c43d12-c0cf-44bc-9d53-5f845956838a" />


### 2) Average age in Aaronberg
- User asked: `What is the average age of customers living in Aaronberg?`
- Copilot answer: `54.9` with a warning about partial model analysis and reduced confidence
<img width="700" height="285.7" alt="image (3)" src="https://github.com/user-attachments/assets/636fb7fa-4631-42c4-b729-dd74380f0b90" />

- Our chatbot answer:
  - `The average age of our customers in Aaronberg is approximately 55 years old.`
  - The system returns the result with confidence and avoids unnecessary doubt
 
<img width="700" height="285.7" alt="image" src="https://github.com/user-attachments/assets/0ce7a9c6-5f76-4c50-b128-fb7bdd3f2b8f" />

### 🎥 Demo
Watch Demo Video:

https://github.com/user-attachments/assets/5128cba5-fe47-4621-b728-7d4b63877b13


## Tech Stack

#### Frontend
- Streamlit

#### API Layer
- FastAPI

#### Orchestration
- LangGraph

#### LLM
- Google Gemini 2.5 Flash

#### Database
- DuckDB

#### Memory
- JSON-based persistent chat storage

#### Language
- Python

## Architecture & Separation of Concerns
The application is built as a modular pipeline with clear responsibilities:

- `frontend/streamlit_app.py`
  - UI layer for users to ask questions and review previous chat history
- `backend/schema_docs`
  - Schema about the dashboard: table name, columns, all transformations done in dashboard(measure, calculated columns etc)
- `backend/app.py`
  - FastAPI middleware exposing chat endpoints
- `backend/graph.py`
  - Graph workflow definition with sequential nodes
- `backend/nodes/` nodes
  - `load_memory.py`: loads existing chat summary and title
  - `retrieve_context.py`: finds schema/dashboard context for the question
  - `generate_sql.py`: synthesizes SQL from the user question and context
  - `run_query.py`: executes the SQL in DuckDB
  - `generate_response.py`: converts query results into a business-friendly answer
  - `summarize_chat.py`: updates conversation summary for memory
  - `save_memory.py`: appends the QA turn to persistent chat storage
  - `title.py`: optionally generates a short title for the chat
- `backend/memory.py`
  - chat persistence helper reading/writing JSON files under `backend/chat_store`
- `backend/state.py`
  - typed state definition for the chat workflow
- `backend/chat_store`
  - runtime json chats storage

## FastAPI Middleware and Endpoints
The backend exposes two endpoints:

- `POST /chat`
  - Payload: `{ "question": "...", "chat_id": "..." }`
  - Returns:
    - `answer`: generated assistant response
    - `sql_query`: SQL used for the analysis
    - `query_result`: result rows from DuckDB
- `GET /chat/{chat_id}`
  - Returns stored chat memory for an existing session
  - Used by the front-end to restore conversation history

## How to Run
1. Clone or open the repository.
2. Install dependencies:

```bash
python -m pip install -r requirements.txt
```

3. Create a `.env` file with your Google API key:

```text
GOOGLE_API_KEY=your_api_key_here
```

4. Start the FastAPI backend:

```bash
uvicorn backend.app:app --reload
```

5. Start the Streamlit frontend:

```bash
streamlit run frontend/streamlit_app.py
```

6. Open the browser UI and ask questions.

## Concept of Chats and Memory
This project tracks conversations as chat sessions:

- Every chat session is identified by `chat_id`
- Chat history is saved as JSON files in `backend/chat_store`
- Each message entry stores:
  - the user question
  - assistant response
  - generated SQL query
  - query result preview
- A summary is kept for the chat so the system can use context across follow-up questions
- This enables conversational BI exploration, not just single-turn queries


## Improvements and Production Considerations
### Improvements
- Add schema-aware SQL validation and stricter prompt safeguards
- Support additional tables, joins, and multi-dataset analysis
- Improve chat summarization with structured metadata instead of free text
- Add authentication and per-user session isolation
- Add caching for repeated analytic queries
- Add more robust error handling for unknown or malformed questions

### Production Considerations
- Replace local DuckDB with a managed analytics database for larger datasets
- Move chat persistence from file JSON to a proper database
- Secure API endpoints with authentication and rate limiting
- Sanitize generated SQL and enforce query policies
- Add logging and monitoring for usage, latency, and query failures
- Use a production-grade deployment strategy (Docker, Kubernetes, cloud service)

## Summary
This repository is a proof-of-concept conversational BI assistant that bridges natural language inputs with live SQL analysis. It uses FastAPI as middleware, DuckDB for query execution, and a node-based workflow to manage memory, context, SQL generation, and response synthesis. The system is built to be more trustworthy than generic Copilot output by returning explicit SQL and chat state memory for every conversation.
