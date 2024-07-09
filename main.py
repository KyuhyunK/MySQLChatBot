import streamlit as st
import plotly.express as px
from database import get_table_columns, run_query
from intents import intents, handle_intent, valid_columns
from openai_utils import invoke_openai_response, invoke_openai_sql, validate_sql_columns
from config import OPENAI_API_KEY, POSTGRESQL_HOST as CONFIG_POSTGRESQL_HOST, POSTGRESQL_USER as CONFIG_POSTGRESQL_USER, POSTGRESQL_PASSWORD as CONFIG_POSTGRESQL_PASSWORD, POSTGRESQL_DATABASE as CONFIG_POSTGRESQL_DATABASE, column_descriptions
import pandas as pd
from sqlalchemy import create_engine

# Function to invoke the chain for generating SQL query and validating it
def invoke_chain(user_question, valid_columns):
    sql_query_prompt = f"Generate a SQL query for the following question: {user_question}. The default table name is 'aggregate_profit_data', unless specified otherwise use this table name. Ensure the query includes the table name and the 'FROM' keyword. Use only valid columns from the following list: {', '.join(valid_columns)}.     
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

    if st.sidebar.button('Show Table Column Descriptions'):
        st.sidebar.write("Table Column Descriptions:")
        for column, description in column_descriptions.items():
            st.sidebar.write(f"**{column}**: {description}")

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
                handle_intent(matched_intent, st)
            else:
                # Generate SQL query using OpenAI (or other method)
                generated_sql_query = invoke_chain(user_question, valid_columns)  # Pass valid_columns as the second argument

                # Run the validated query and display the results
                df = run_query(generated_sql_query)
                response_prompt = (
                        f"User question: {user_question}\nSQL Query: {generated_sql_query}\n"
                        "Generate a suitable explanation for this query. Use the following Python code to display the table:\n\n"
                        "st.dataframe(df)\n\n"
                        "Always show the graphs generated from plotly when applicable. "
                        "Then write a brief description about the graph/table. Keep your response concise and easy to understand."
                    )

                response = invoke_openai_response(response_prompt)
                
                st.write("Generated SQL Query:")
                st.code(generated_sql_query)
                
                if not df.empty:
                    st.write("Table:")
                    st.dataframe(df)  # Use Streamlit's dataframe to display the dataframe
                    graph_type = determine_graph_type(df)
                    fig = create_plotly_graph(df, graph_type, "listing_state", "total_revenue", "Total Revenue by Listing State")
                    st.plotly_chart(fig)
                    st.write("Description: This graph shows the total revenue by listing state based on the queried data.")
        else:
            st.write("Please enter a valid question.")

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