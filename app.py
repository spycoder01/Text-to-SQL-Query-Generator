import streamlit as st
import pandas as pd

from gemini import generate_sql
from database import execute_query


st.title("Text-to-SQL Query Generator")

st.write(
    "Ask a question about the employee database in natural language."
)


question = st.text_input(
    "Enter your question:"
)


if st.button("Run Query"):

    if question:

        try:

            # Generate SQL using Gemini
            sql = generate_sql(question)

            st.subheader("Generated SQL")

            st.code(sql, language="sql")


            # Execute SQL in MySQL
            columns, results = execute_query(sql)


            # Convert result into DataFrame
            df = pd.DataFrame(
                results,
                columns=columns
            )


            st.subheader("Result")

            st.dataframe(df, use_container_width=True)


        except Exception as e:

            st.error(f"Error: {e}")

    else:

        st.warning("Please enter a question.")