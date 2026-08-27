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