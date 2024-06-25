import mysql.connector
from mysql.connector import Error
import pandas as pd
from config import MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DATABASE

def create_mysql_connection():
    connection = None
    try:
        connection = mysql.connector.connect(
            host=MYSQL_HOST,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD,
            database=MYSQL_DATABASE
        )
        if connection.is_connected():
            print("MySQL connection successful")
    except Error as e:
        print(f"Error: '{e}'")
    return connection

def get_table_columns():
    connection = create_mysql_connection()
    cursor = connection.cursor()
    query = "DESCRIBE aggregate_profit_data"
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()
    connection.close()
    columns_df = pd.DataFrame(result, columns=["Field", "Type", "Null", "Key", "Default", "Extra"])
    return columns_df

def run_query(query):
    connection = create_mysql_connection()
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        df = pd.DataFrame(result, columns=columns)
    except Error as e:
        print(f"Error: '{e}'")
        df = pd.DataFrame()
        result = []
    finally:
        cursor.close()
        connection.close()
    return df, result
