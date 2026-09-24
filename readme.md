# AI-Powered SQL Query Generator

An **LLM-powered natural-language-to-SQL application** that converts business questions into executable MySQL queries using **Ollama + Qwen 2.5**, with a **FastAPI backend** and **Streamlit frontend**.

## 🚀 Overview

The application allows users to interact with a MySQL database using natural language instead of manually writing SQL queries.

**Workflow:**

`Natural Language → Qwen 2.5 → SQL Query → Validation → MySQL → Results`

The project uses a customer churn dataset containing **7,043 records and 21 attributes**.

---

## ✨ Features

* 🧠 **Natural Language → SQL** using Ollama and Qwen 2.5
* 🔍 **Dynamic database and schema discovery**
* 🛡️ **Read-only SQL validation** to prevent write operations
* ⚡ **SQL query execution** through MySQL
* 💡 **Automatic SQL explanations**
* 📊 **Query result visualization**
* 📁 **CSV export**
* 📝 **Query history**
* 🌐 **FastAPI REST backend**
* 🖥️ **Streamlit interactive frontend**

---

## 🛠️ Tech Stack

| Category          | Technologies |
| ----------------- | ------------ |
| Programming       | Python       |
| LLM               | Qwen 2.5     |
| Local LLM Runtime | Ollama       |
| Backend           | FastAPI      |
| Frontend          | Streamlit    |
| Database          | MySQL        |
| Database ORM      | SQLAlchemy   |
| Data Processing   | Pandas       |
| API Communication | Requests     |
| SQL Parsing       | SQLParse     |

---

## 📂 Project Structure

```text
AI-Powered-SQL-Generator/
│
├── app.py                 # FastAPI backend
├── ui.py                  # Streamlit frontend
├── query_generator.py     # LLM-based SQL generation & execution
├── databases.py           # Database connection & schema discovery
├── requirements.txt       # Python dependencies
├── README.md              # Project documentation
└── .gitignore             # Ignored files & secrets
```

---

## ⚙️ Setup & Installation

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/AI-Powered-SQL-Generator.git
cd AI-Powered-SQL-Generator
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Install Ollama

Install Ollama and download the Qwen 2.5 model:

```bash
ollama pull qwen2.5:3b
```

Verify the model:

```bash
ollama list
```

---

## 🔐 Environment Variables

Create a `.env` file in the project root:

```env
MYSQL_HOST=localhost
MYSQL_USER=root
MYSQL_PASSWORD=YOUR_MYSQL_PASSWORD
MYSQL_DATABASE=churnanalysis
MYSQL_PORT=3306
```

⚠️ **Never commit `.env` or database credentials to GitHub.**

---

## 🗄️ Database

The application currently uses a customer churn dataset stored in MySQL.

**Database:**

```text
churnanalysis
```

**Table:**

```text
churnnn
```

**Dataset:**

* 7,043 customer records
* 21 attributes
* Customer demographics
* Services
* Contract information
* Payment methods
* Monthly charges
* Churn status

---

## ▶️ Running the Application

### Start FastAPI

Open a terminal and run:

```bash
python -m uvicorn app:app --reload
```

Backend:

```text
http://127.0.0.1:8000
```

### Start Streamlit

Open another terminal:

```bash
python -m streamlit run ui.py
```

Frontend:

```text
http://localhost:8501
```

---

## 💬 Example Queries

Users can ask questions such as:

```text
Show the number of customers who churned
```

```text
Show churned customers by payment method
```

```text
What is the average monthly charge of churned customers?
```

```text
Show the number of customers in each contract type
```

```text
Show churned customers for each contract type
```

The system converts these natural-language requests into SQL queries and executes them against MySQL.

---

## 📊 Sample Results

### Overall Churn

| Metric                        | Result |
| ----------------------------- | -----: |
| Total Customers               |  7,043 |
| Churned Customers             |  1,869 |
| Churn Rate                    | 26.54% |
| Avg. Monthly Charge — Churned |  74.44 |

### Churn by Payment Method

| Payment Method   | Churned Customers |
| ---------------- | ----------------: |
| Electronic Check |             1,071 |
| Mailed Check     |               308 |
| Bank Transfer    |               258 |
| Credit Card      |               232 |

---

## 🔒 SQL Safety

The application restricts generated queries to **read-only SQL operations**.

The validation layer prevents potentially destructive operations such as:

```text
INSERT
UPDATE
DELETE
DROP
ALTER
TRUNCATE
CREATE
GRANT
REVOKE
REPLACE
```

It also validates that generated queries use the expected database table.

---

## 🏗️ Architecture

```text
                ┌─────────────────────┐
                │   Streamlit UI      │
                │   Natural Language  │
                └──────────┬──────────┘
                           │
                           ▼
                ┌─────────────────────┐
                │    FastAPI API      │
                └──────────┬──────────┘
                           │
                           ▼
                ┌─────────────────────┐
                │  Ollama + Qwen 2.5 │
                │    SQL Generation   │
                └──────────┬──────────┘
                           │
                           ▼
                ┌─────────────────────┐
                │   SQL Validation    │
                └──────────┬──────────┘
                           │
                           ▼
                ┌─────────────────────┐
                │     MySQL DB        │
                │     churnnn         │
                └──────────┬──────────┘
                           │
                           ▼
                ┌─────────────────────┐
                │ Results / CSV Export│
                └─────────────────────┘
```

---

## 📈 Key Outcomes

* Processed **7,043 customer records** across **21 attributes**.
* Generated and executed SQL from natural-language questions.
* Identified **1,869 churned customers (26.54%)**.
* Identified **1,071 churned customers using electronic check**.
* Implemented read-only SQL validation for safer database interaction.

---

## 🔮 Future Improvements

* Support multiple databases and tables
* Add query caching for faster repeated queries
* Add advanced data visualizations
* Improve SQL generation accuracy
* Add authentication and role-based access
* Deploy the application with a cloud-hosted database and LLM
* Add automated SQL error correction

---

## 👩‍💻 Author

**Sachi Wadajkar**

B.Tech — Chemical Engineering
IIT (BHU), Varanasi

---

## ⭐ Project Highlights

**Natural Language → SQL → Database → Analytics**

Built to simplify SQL-based data analysis for users who can describe business questions but may not know SQL.

