from google import genai
from dotenv import load_dotenv
import os

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


def generate_sql(question, schema):

    prompt = f"""
You are an expert MySQL SQL developer.

Convert the user's question into a MySQL SQL query.

Database schema:
{schema}

Rules:
1. Generate only the SQL query.
2. Do not use markdown.
3. Do not explain the query.
4. Use MySQL syntax.
5. Only generate SELECT queries.
6. Format the SQL query for readability.
7. Put each major SQL clause on a separate line.
8. Keep the JOIN condition on a separate line after JOIN.
9. Do not unnecessarily break simple expressions across multiple lines.
10. Use only tables and columns present in the provided schema.

User question:
{question}
"""

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt
    )

    return response.text.strip()