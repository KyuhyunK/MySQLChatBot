import streamlit as st
import plotly.express as px
import torch
import logging
import requests
from database import get_table_columns, run_query
from intents import intents, valid_columns
from openai_utils import invoke_openai_response, invoke_openai_sql, validate_sql_columns
from config import POSTGRESQL_HOST as CONFIG_POSTGRESQL_HOST, POSTGRESQL_USER as CONFIG_POSTGRESQL_USER, POSTGRESQL_PASSWORD as CONFIG_POSTGRESQL_PASSWORD, POSTGRESQL_DATABASE as CONFIG_POSTGRESQL_DATABASE
import pandas as pd
from sqlalchemy import create_engine

# Function to check internet connection
def check_internet_connection():
    url = "http://www.google.com"
    timeout = 5
    try:
        request = requests.get(url, timeout=timeout)
        return True
    except (requests.ConnectionError, requests.Timeout) as exception:
        return False

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Function to invoke the chain for generating SQL query and validating it
def invoke_chain(user_question, valid_columns):
    sql_query_prompt = f"Generate a SQL query for the following question: {user_question}. The default table name is 'aggregate_profit_data', unless specified otherwise use this table name. Ensure the query includes the table name and the 'FROM' keyword. Use only valid columns from the following list: {', '.join(valid_columns)}. Keep your response concise and easy to understand."
    
    generated_sql_query = invoke_openai_sql(sql_query_prompt)
    corrected_sql_query = validate_sql_columns(generated_sql_query, valid_columns)
    return corrected_sql_query

def main():
    st.title("SQL Query Generator")

    st.sidebar.title("Settings")
    st.sidebar.write("Configure your database connection below:")

    POSTGRESQL_HOST = st.sidebar.text_input("PostgreSQL Host", value=CONFIG_POSTGRESQL_HOST)
    POSTGRESQL_USER = st.sidebar.text_input("PostgreSQL User", value=CONFIG_POSTGRESQL_USER)
    POSTGRESQL_PASSWORD = st.sidebar.text_input("PostgreSQL Password", value=CONFIG_POSTGRESQL_PASSWORD)
    POSTGRESQL_DATABASE = st.sidebar.text_input("PostgreSQL Database", value=CONFIG_POSTGRESQL_DATABASE)

    try:
        engine = create_engine(f'postgresql://{POSTGRESQL_USER}:{POSTGRESQL_PASSWORD}@{POSTGRESQL_HOST}/{POSTGRESQL_DATABASE}')
        st.success("Connected to the database successfully.")
    except Exception as e:
        st.error(f"Error: {e}")

    user_question = st.text_input("Enter your question about the database:")
    if st.button('Submit'):
        if user_question:
            matched_intent = None
            for intent in intents:
                if any(pattern.lower() in user_question.lower() for pattern in intent['patterns']):
                    matched_intent = intent
                    break

            if matched_intent:
                endpoint = matched_intent['endpoint']
                params = matched_intent['params']
                response = invoke_openai_response(f"Endpoint: {endpoint}, Params: {params}")
                st.write("Model Response:")
                st.json(response)
            else:
                corrected_sql_query = invoke_chain(user_question, valid_columns=[])
                df = run_query(corrected_sql_query)
                response_prompt = f"User question: {user_question}\nSQL Query: {corrected_sql_query}\nGenerate a suitable explanation for this query."
                response = invoke_openai_response(response_prompt)
                st.write("Generated SQL Query:")
                st.code(corrected_sql_query)
                if not df.empty:
                    st.dataframe(df)
                    graph_type = determine_graph_type(user_question)
                    if 'listing_state' in df.columns and 'revenue_difference' in df.columns:
                        create_plotly_graph(df, graph_type, "listing_state", "revenue_difference", "Total Revenue Difference by Listing State")

if __name__ == "__main__":
    main()

st.write("Example Queries:")
st.write("What is the total revenue by listing state?")
st.write("Which are the top 10 SKUs by total profit?")
st.write("Can you show me the quarterly revenue trend?")
st.write("What are the top 5 ASINs by total ordered items?")
st.write("Can you create a graph that shows the difference in revenue by listing state?")
