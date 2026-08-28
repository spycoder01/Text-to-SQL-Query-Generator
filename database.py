import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()


def get_connection():

    connection = mysql.connector.connect(
        host=os.getenv("MYSQL_HOST"),
        user=os.getenv("MYSQL_USER"),
        password=os.getenv("MYSQL_PASSWORD"),
        database=os.getenv("MYSQL_DATABASE")
    )

    return connection


def execute_query(sql):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(sql)

    results = cursor.fetchall()
    columns = cursor.column_names

    cursor.close()
    connection.close()

    return columns, results

def get_schema():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT 
            TABLE_NAME,
            COLUMN_NAME,
            DATA_TYPE
        FROM INFORMATION_SCHEMA.COLUMNS
        WHERE TABLE_SCHEMA = DATABASE()
        ORDER BY TABLE_NAME, ORDINAL_POSITION
    """)

    results = cursor.fetchall()

    cursor.close()
    connection.close()

    return results


def format_schema(schema):

    formatted_schema = ""

    current_table = None

    for table, column, data_type in schema:

        if table != current_table:

            formatted_schema += f"\nTable: {table}\n"
            formatted_schema += "Columns:\n"

            current_table = table

        formatted_schema += f"- {column} ({data_type})\n"

    return formatted_schema

# Test
schema = get_schema()

formatted_schema = format_schema(schema)

print(formatted_schema)