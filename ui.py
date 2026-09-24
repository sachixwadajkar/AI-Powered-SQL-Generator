import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"

st.title("AI-Powered SQL Query Generator")

# Query history storage
if "history" not in st.session_state:
    st.session_state["history"] = []
if "sqlquery" not in st.session_state:
    st.session_state["sqlquery"] = ""
if "last_results" not in st.session_state:
    st.session_state["last_results"] = []

# Database selection
databases = requests.get(f"{API_URL}/databases").json()
database = st.selectbox("Select Database", databases)
tables = requests.get(f"{API_URL}/tables/{database}").json() if database else []
table = st.selectbox("Select Table", tables) if tables else None
columns = requests.get(f"{API_URL}/columns/{database}/{table}").json() if table else []
if columns:
    st.write(f"Columns in table: {columns}")

# User natural language input
query = st.text_area("Enter your query in natural language:")

if st.button("Generate SQL"):
    response = requests.post(f"{API_URL}/generate_sql", json={"query": query})
    if response.status_code == 200:
        sql = response.json().get("sql")
        explanation = response.json().get("explanation")
        st.code(sql, language="sql")
        st.info(f"Explanation: {explanation}")
        st.session_state["sqlquery"] = sql
        st.session_state["history"].append({"query": query, "sql": sql, "explanation": explanation})
    else:
        st.error("Error generating SQL.")

if st.session_state.get("sqlquery"):
    if st.button("Execute SQL"):
        response = requests.post(f"{API_URL}/execute_sql", json={"query": st.session_state["sqlquery"]})
        if response.status_code == 200:
            results = response.json().get("results")
            csv_data = response.json().get("csv")
            st.session_state["last_results"] = results
            if results and isinstance(results, list):
                st.dataframe(results)
                st.download_button("Download Results as CSV", csv_data, file_name="results.csv")
            else:
                st.info(str(results))
        else:
            st.error("Error executing SQL.")

# Query history
if st.session_state["history"]:
    st.subheader("Query History")
    for i, h in enumerate(st.session_state["history"][::-1], 1):
        st.markdown(f"**{i}. NL:** {h['query']}")
        st.code(h['sql'], language="sql")
        st.write(f"*Explanation:* {h['explanation']}")
        st.write("---")
