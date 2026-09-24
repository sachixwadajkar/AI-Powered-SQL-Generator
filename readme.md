# AI-Powered SQL Query Generator

A modern tool to generate, explain, and run SQL queries from plain English powered by advanced LLMs. Features a simple web UI, result downloading, and query history.

## Features

- 🌟 Natural language to SQL generation (via LLM)
- ✍️ Easy-to-understand SQL query explanations
- 🗂️ Browse DB schema (database, tables, columns)
- 📥 Download query results as CSV
- 🔄 Query history tracking for every session
- Responsive Streamlit interface
- Modular FastAPI backend

## Setup Instructions

1. Clone this repo and install dependencies:
    ```
    git clone <your_repo_url>
    cd ai-sql-query-generator
    pip install -r requirements.txt
    ```

2. Setup `.env` for all necessary keys and DB credentials:
    ```
    MYSQL_HOST=...
    MYSQL_USER=...
    MYSQL_PASSWORD=...
    MYSQL_DATABASE=...
    MYSQL_PORT=...
    OPENAI_API_KEY=...
    ```

3. Start FastAPI backend:
    ```
    uvicorn app:app --reload
    ```

4. Start the Streamlit app:
    ```
    streamlit run ui.py
    ```

5. Point browser to [localhost:8501](http://localhost:8501).

## API Endpoints

- `GET /databases`  
- `GET /tables/{database}`
- `GET /columns/{database}/{table}`
- `POST /generate_sql`
- `POST /execute_sql`

## Customizing & Extending

- Add authentication, multiple DB support, or role-based access in the FastAPI backend
- Improve UI/UX with more Streamlit or React features
- Swap LLM models in `query_generator.py` for other providers

---

**Now you're ready to use and extend your AI SQL assistant!**
