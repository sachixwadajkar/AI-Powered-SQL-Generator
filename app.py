from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from query_generator import generate_sql_query, execute_query, explain_sql_query, results_to_csv
from databases import list_databases, list_tables, list_columns

app = FastAPI()

class QueryRequest(BaseModel):
    query: str

@app.get("/databases")
def get_databases():
    return list_databases()

@app.get("/tables/{database_name}")
def get_tables(database_name: str):
    return list_tables(database_name)

@app.get("/columns/{database_name}/{table_name}")
def get_columns(database_name: str, table_name: str):
    return list_columns(database_name, table_name)

@app.post("/generate_sql")
def generate_sql_endpoint(req: QueryRequest):
    try:
        sql = generate_sql_query(req.query)
        explanation = explain_sql_query(sql)
        return {"sql": sql, "explanation": explanation}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/execute_sql")
def execute_sql_endpoint(req: QueryRequest):
    try:
        rows = execute_query(req.query)
        csv_data = results_to_csv(rows) if isinstance(rows, list) else ""
        return {"results": rows, "csv": csv_data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
