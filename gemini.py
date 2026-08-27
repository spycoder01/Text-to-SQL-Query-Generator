from google import genai
from dotenv import load_dotenv
import os

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


def generate_sql(question):

    prompt = f"""
You are an expert MySQL SQL developer.

Convert the user's question into a MySQL SQL query.

Database schema:

Table: employees

Columns:
- employee_id INT
- name VARCHAR(100)
- department VARCHAR(100)
- salary INT
- age INT

Rules:
1. Generate only the SQL query.
2. Do not use markdown.
3. Do not explain the query.
4. Use MySQL syntax.
5. Only generate SELECT queries.
6. Format the SQL query across multiple lines for readability.
7. Put each major SQL clause on a separate line.
8. Use proper indentation.

User question:
{question}
"""

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt
    )

    return response.text.strip()