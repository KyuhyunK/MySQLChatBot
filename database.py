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
        else:
            print("Failed to connect to MySQL")
    except Error as e:
        print(f"Error: '{e}'")
    return connection

def get_table_columns():
    connection = create_mysql_connection()
    if connection is None:
        print("Error: Connection to MySQL is not established.")
        return pd.DataFrame(), []

    cursor = connection.cursor()
    try:
        query = "DESCRIBE aggregate_profit_data"
        cursor.execute(query)
        result = cursor.fetchall()
        columns_df = pd.DataFrame(result, columns=["Field", "Type", "Null", "Key", "Default", "Extra"])
        print("Columns DataFrame:\n", columns_df)  # Debugging: Print the DataFrame
    except Error as e:
        print(f"Error: '{e}'")
        columns_df = pd.DataFrame()
    finally:
        cursor.close()
        connection.close()
    return columns_df

def run_query(query):
    connection = create_mysql_connection()
    if connection is None:
        print("Error: Connection to MySQL is not established.")
        return pd.DataFrame(), []

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
