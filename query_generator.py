import os
import re
import requests
import pandas as pd

from dotenv import load_dotenv
from databases import engine, list_databases, list_tables, list_columns
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import text

load_dotenv()

OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "qwen2.5:3b"

DATABASE_NAME = os.getenv("MYSQL_DATABASE", "churnanalysis")
TABLE_NAME = "churnnn"


def clean_sql_output(sql_text):
    """Remove markdown/code fences and return clean SQL."""
    sql_text = sql_text.strip()

    sql_text = re.sub(
        r"```(?:sql)?",
        "",
        sql_text,
        flags=re.IGNORECASE
    )

    sql_text = sql_text.replace("```", "").strip()

    # If the model added explanation before SELECT,
    # keep only the SQL portion.
    match = re.search(
        r"(SELECT\b.*)",
        sql_text,
        flags=re.IGNORECASE | re.DOTALL
    )

    if match:
        sql_text = match.group(1).strip()

    return sql_text


def get_schema():
    """Retrieve the actual schema from MySQL."""

    tables = list_tables(DATABASE_NAME)

    if TABLE_NAME not in tables:
        raise ValueError(
            f"Table '{TABLE_NAME}' was not found in database "
            f"'{DATABASE_NAME}'. Available tables: {tables}"
        )

    columns = list_columns(DATABASE_NAME, TABLE_NAME)

    return columns


def generate_sql_query(natural_language_query):
    """Convert natural language into SQL using local Ollama model."""

    columns = get_schema()

    schema_info = (
        f"Database: {DATABASE_NAME}\n"
        f"Table: {TABLE_NAME}\n"
        f"Columns: {', '.join(columns)}"
    )

    prompt = f"""
You are an expert MySQL SQL generator.

Your task is to convert the user's natural-language request
into ONE executable MySQL SELECT query.

ACTUAL DATABASE SCHEMA:
{schema_info}

STRICT RULES:

1. Use ONLY the table '{TABLE_NAME}'.
2. Use ONLY the columns listed above.
3. NEVER invent a table name.
4. NEVER invent a column name.
5. The database is MySQL.
6. Generate ONLY a SELECT query.
7. Do NOT generate INSERT, UPDATE, DELETE, DROP, ALTER,
   CREATE, TRUNCATE, GRANT, or other write operations.
8. Do NOT include markdown.
9. Do NOT include explanations.
10. Return ONLY the SQL query.
11. The table contains customer churn data.
12. IMPORTANT: The Churn column is encoded as:
    - Churn = '1' means the customer churned.
    - Churn = '0' means the customer did not churn.
13. Churn is stored as a text column, so compare it using '1' or '0'.

USER REQUEST: {natural_language_query}

SQL:
"""

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": OLLAMA_MODEL,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": 0
            }
        },
        timeout=120
    )

    response.raise_for_status()

    raw_sql = response.json()["response"]

    sql = clean_sql_output(raw_sql)

    # Basic safety validation
    validate_sql(sql)

    return sql


def validate_sql(sql_query):
    """Allow only read-only SELECT queries."""

    normalized = sql_query.strip().lower()

    if not normalized.startswith("select"):
        raise ValueError(
            "Only SELECT queries are allowed."
        )

    forbidden = [
        "insert ",
        "update ",
        "delete ",
        "drop ",
        "alter ",
        "truncate ",
        "create ",
        "grant ",
        "revoke ",
        "replace ",
    ]

    for keyword in forbidden:
        if keyword in normalized:
            raise ValueError(
                f"Unsafe SQL operation detected: {keyword.strip()}"
            )

    # Prevent queries from accessing arbitrary tables
    allowed_table = TABLE_NAME.lower()

    table_pattern = re.findall(
        r"(?:from|join)\s+([a-zA-Z0-9_.`]+)",
        normalized
    )

    for table in table_pattern:
        clean_table = table.replace("`", "").split(".")[-1]

        if clean_table != allowed_table:
            raise ValueError(
                f"Generated query attempted to access "
                f"unauthorized table: {table}"
            )


def explain_sql_query(sql):
    """Explain SQL using the same local Ollama model."""

    prompt = f"""
You are an SQL expert.

Explain this MySQL query in simple English.

SQL:
{sql}

Explain:
1. What data it retrieves.
2. What filtering it performs.
3. Any aggregation or grouping.
4. What the final result represents.

Keep the explanation concise.

Do not generate another SQL query.
"""

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": OLLAMA_MODEL,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": 0,
                "num_predict": 80
            }
        },
        timeout=120
    )

    response.raise_for_status()

    return response.json()["response"].strip()


def execute_query(sql_query):
    """Execute a validated read-only SQL query."""

    try:
        validate_sql(sql_query)

        with engine.connect() as conn:
            result = conn.execute(text(sql_query))

            rows = [
                dict(row._mapping)
                for row in result
            ]

        return rows

    except (SQLAlchemyError, ValueError) as e:
        return f"SQL Execution Error: {str(e)}"


def results_to_csv(results):
    """Convert SQL results to CSV."""

    if not isinstance(results, list) or len(results) == 0:
        return ""

    df = pd.DataFrame(results)

    return df.to_csv(index=False)