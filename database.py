import psycopg2
import pandas as pd
from openai_utils import validate_sql_columns
from config import POSTGRESQL_HOST, POSTGRESQL_PORT, POSTGRESQL_USER, POSTGRESQL_PASSWORD, POSTGRESQL_DATABASE



def create_pg_connection():
    connection = None
    try:
        connection = psycopg2.connect(
            host=POSTGRESQL_HOST,
	    port=POSTGRESQL_PORT,
            user=POSTGRESQL_USER,
            password=POSTGRESQL_PASSWORD,
            dbname=POSTGRESQL_DATABASE
        )
        if connection:
            print("PostgreSQL connection successful")
        else:
            print("Failed to connect to PostgreSQL")
    except Exception as e:
        print(f"Error: '{e}'")
    return connection

def get_table_columns():
    connection = create_pg_connection()
    if connection is None:
        print("Error: Connection to PostgreSQL is not established.")
        return pd.DataFrame()

    cursor = connection.cursor()
    try:
        query = "SELECT column_name FROM information_schema.columns WHERE table_name = 'aggregate_profit_data'"
        cursor.execute(query)
        result = cursor.fetchall()
        columns_df = pd.DataFrame(result, columns=["Column"])
    except Exception as e:
        print(f"Error: '{e}'")
        columns_df = pd.DataFrame()
    finally:
        cursor.close()
        connection.close()
    return columns_df

def run_query(query):
    connection = create_pg_connection()
    if connection is None:
        print("Error: Connection to PostgreSQL is not established.")
        return pd.DataFrame()

    cursor = connection.cursor()
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        df = pd.DataFrame(result, columns=columns)
    except Exception as e:
        print(f"Error: '{e}'")
        df = pd.DataFrame()
    finally:
        cursor.close()
        connection.close()
    return df
