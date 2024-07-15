import streamlit as st
import plotly.express as px
from database import get_table_columns, run_query
from intents import intents, handle_intent, valid_columns
from openai_utils import invoke_openai_response, invoke_openai_sql, validate_sql_columns
from config import OPENAI_API_KEY, POSTGRESQL_HOST as CONFIG_POSTGRESQL_HOST, POSTGRESQL_USER as CONFIG_POSTGRESQL_USER, POSTGRESQL_PASSWORD as CONFIG_POSTGRESQL_PASSWORD, POSTGRESQL_DATABASE as CONFIG_POSTGRESQL_DATABASE, column_descriptions
import pandas as pd
from sqlalchemy import create_engine
import re

# Secret token
SECRET_TOKEN = "happysun"

# Function to invoke the chain for generating SQL query and validating it
def invoke_chain(user_question, valid_columns):
    sql_query_prompt = (
        f"Generate a SQL query for the following question: {user_question}. "
        f"The default table name is 'aggregate_profit_data', unless specified otherwise use this table name. "
        f"Ensure the query includes the table name and the 'FROM' keyword. "
        f"Use only valid columns from the following list: {', '.join(valid_columns)}. "
        f"All columns are of type TEXT, so ensure numbers are enclosed in quotes in the query to handle them as text."
    )
    generated_sql_query = invoke_openai_sql(sql_query_prompt)
    corrected_sql_query = validate_sql_columns(generated_sql_query, valid_columns)
    return corrected_sql_query

@st.cache_data
def cached_run_query(query):
    return run_query(query)

def adjust_query(query):
    # Ensure proper data type casting for numeric operations
    query = re.sub(r'SUM\(([^)]+)\)', r'SUM(CAST(\1 AS numeric))', query)
    return query

def remove_backticks(query):
    # Remove any backticks from the query string
    return query.replace('`', '')

def split_query_and_description(response):
    # Split the response into query and description parts
    parts = response.split("```")
    query = parts[0].strip()
    description = parts[1].strip() if len(parts) > 1 else ""
    return query, description

def main():
    # Check for secret token in URL
    query_params = st.experimental_get_query_params()
    if "token" in query_params and query_params["token"][0] == SECRET_TOKEN:
        st.title("SQL Query Generator")

        st.sidebar.title("Settings")
        st.sidebar.write("Configure your database connection below:")

        POSTGRESQL_HOST = st.sidebar.text_input("PostgreSQL Host", value=CONFIG_POSTGRESQL_HOST)
        POSTGRESQL_USER = st.sidebar.text_input("PostgreSQL User", value=CONFIG_POSTGRESQL_USER)
        POSTGRESQL_PASSWORD = st.sidebar.text_input("PostgreSQL Password", value=CONFIG_POSTGRESQL_PASSWORD)
        POSTGRESQL_DATABASE = st.sidebar.text_input("PostgreSQL Database", value=CONFIG_POSTGRESQL_DATABASE)

        if st.sidebar.button('Show Table Column Descriptions'):
            st.sidebar.write("Table Column Descriptions:")
            for column, description in column_descriptions.items():
                st.sidebar.write(f"**{column}**: {description}")

        try:
            engine = create_engine(f'postgresql://{POSTGRESQL_USER}:{POSTGRESQL_PASSWORD}@{POSTGRESQL_HOST}/{POSTGRESQL_DATABASE}')
            st.success("Connected to the database successfully.")
        except Exception as e:
            st.error(f"Error: {e}")
            st.stop()  # Stop execution if connection fails

        user_question = st.text_input("Enter your question about the database:")
        if st.button('Submit'):
            if user_question:
                matched_intent = None
                for intent in intents:
                    if any(pattern.lower() in user_question.lower() for pattern in intent['patterns']):
                        matched_intent = intent
                        break

                if matched_intent:
                    handle_intent(matched_intent, st)
                else:
                    # Generate SQL query using OpenAI (or other method)
                    generated_sql_query = invoke_chain(user_question, valid_columns)
                    adjusted_sql_query = adjust_query(generated_sql_query)

                    # Remove backticks from the generated SQL query
                    adjusted_sql_query = remove_backticks(adjusted_sql_query)
                    
                    # Split the query and description if present
                    final_query, query_description = split_query_and_description(adjusted_sql_query)

                    # Display the generated SQL query without backticks
                    st.write("Generated SQL Query:")
                    st.code(final_query)

                    # Run the validated query and display the results
                    df = cached_run_query(final_query)
                    st.write(f"DataFrame shape: {df.shape}")

                    if not df.empty:
                        st.write("Table:")
                        st.dataframe(df)

                        st.write("Query Description:")
                        st.write(query_description)

                        # Determine columns for dynamic plotting
                        columns = df.columns
                        if len(columns) >= 2:
                            x_col = columns[0]
                            y_col = columns[1]
                            graph_type = determine_graph_type(df)
                            fig = create_plotly_graph(df, graph_type, x_col, y_col, f"Graph for {x_col} vs {y_col}")
                            st.plotly_chart(fig)
                            st.write(f"Description: This graph shows the relationship between {x_col} and {y_col} based on the queried data.")
                    else:
                        st.write("No data returned from the query.")
            else:
                st.write("Please enter a valid question.")
    else:
        st.error("Unauthorized access. Please use the correct link to access this application.")

def create_plotly_graph(df, graph_type, x_col, y_col, title):
    if graph_type == 'bar':
        fig = px.bar(df, x=x_col, y=y_col, title=title)
    elif graph_type == 'line':
        fig = px.line(df, x=x_col, y=y_col, title=title)
    elif graph_type == 'scatter':
        fig = px.scatter(df, x=x_col, y=y_col, title=title)
    else:
        fig = px.histogram(df, x=x_col, y=y_col, title=title)
    return fig

def determine_graph_type(df):
    if len(df.columns) == 2:
        if df.columns[1].endswith('_revenue') or df.columns[1].endswith('_profit'):
            return 'bar'
        elif df.columns[1].endswith('_trend'):
            return 'line'
        else:
            return 'scatter'
    else:
        return 'bar'

if __name__ == "__main__":
    main()

st.write("Example Queries:")
st.write("What is the total revenue by listing state?")
st.write("Which are the top 10 SKUs by total profit?")
st.write("Can you show me the quarterly revenue trend?")
st.write("What are the top 5 ASINs by total ordered items?")
st.write("Can you create a graph that shows the difference in revenue by listing state?")
