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

    # Get columns and primary keys
    cursor.execute("""
        SELECT
            TABLE_NAME,
            COLUMN_NAME,
            DATA_TYPE,
            COLUMN_KEY
        FROM INFORMATION_SCHEMA.COLUMNS
        WHERE TABLE_SCHEMA = DATABASE()
        ORDER BY TABLE_NAME, ORDINAL_POSITION
    """)

    columns = cursor.fetchall()

    # Get foreign key relationships
    cursor.execute("""
        SELECT
            TABLE_NAME,
            COLUMN_NAME,
            REFERENCED_TABLE_NAME,
            REFERENCED_COLUMN_NAME
        FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE
        WHERE TABLE_SCHEMA = DATABASE()
        AND REFERENCED_TABLE_NAME IS NOT NULL
    """)

    foreign_keys = cursor.fetchall()

    cursor.close()
    connection.close()

    return columns, foreign_keys


def format_schema(columns, foreign_keys):

    formatted_schema = ""

    current_table = None

    for table, column, data_type, column_key in columns:

        if table != current_table:

            formatted_schema += f"\nTable: {table}\n"
            formatted_schema += "Columns:\n"

            current_table = table

        key_info = ""

        if column_key == "PRI":
            key_info = " PRIMARY KEY"

        formatted_schema += (
            f"- {column} ({data_type}){key_info}\n"
        )

    if foreign_keys:

        formatted_schema += "\nRelationships:\n"

        for table, column, ref_table, ref_column in foreign_keys:

            formatted_schema += (
                f"- {table}.{column} → "
                f"{ref_table}.{ref_column}\n"
            )

    return formatted_schema

# Test
columns, foreign_keys = get_schema()

formatted_schema = format_schema(
    columns,
    foreign_keys
)

print(formatted_schema)