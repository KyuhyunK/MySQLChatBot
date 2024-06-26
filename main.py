import streamlit as st
import plotly.express as px
from database import get_table_columns, run_query
from intents import intents, valid_columns
from amazonapi import get_amazon_data
import requests

# Load secrets from Streamlit secrets management
rapidapi_key = st.secrets["rapidapi"]["RAPIDAPI_KEY"]

def determine_graph_type(user_question):
    if "line graph" in user_question.lower():
        return "line"
    elif "bar chart" in user_question.lower():
        return "bar"
    elif "column chart" in user_question.lower():
        return "column"
    elif "pie chart" in user_question.lower():
        return "pie"
    elif "area chart" in user_question.lower():
        return "area"
    elif "scatter plot" in user_question.lower():
        return "scatter"
    else:
        return "bar"

def create_plotly_graph(df, graph_type, x_col, y_col, title):
    if graph_type == "bar":
        fig = px.bar(df, x=x_col, y=y_col, title=title)
    elif graph_type == "line":
        fig = px.line(df, x=x_col, y=y_col, title=title)
    elif graph_type == "column":
        fig = px.bar(df, x=x_col, y=y_col, title=title)
    elif graph_type == "pie":
        fig = px.pie(df, names=x_col, values=y_col, title=title)
    elif graph_type == "area":
        fig = px.area(df, x=x_col, y=y_col, title=title)
    elif graph_type == "scatter":
        fig = px.scatter(df, x=x_col, y=y_col, title=title)
    else:
        st.write("Unsupported graph type")
        return
    st.plotly_chart(fig)

st.title('AI Chat Interface for MySQL Database')

st.write("Welcome to the AI Chat Interface for MySQL Database. You can ask questions about the database, and I will help you retrieve and visualize the data. \n") 

if st.button('Show Table Structure'):
    columns_df = get_table_columns()
    st.write("Table Structure of 'aggregate_profit_data':")
    st.write(columns_df)
    st.write("Column Descriptions:")
    for col in columns_df["Field"]:
        st.write(f"**{col}**: {column_descriptions.get(col, 'No description available')}")

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
            data = get_amazon_data(endpoint, params)
            st.write("Amazon API Response:")
            st.json(data)
            # Additional processing and visualization if needed
        else:
            corrected_sql_query = invoke_chain(user_question, valid_columns)
            df, result = run_query(corrected_sql_query)
            response_prompt = f"User question: {user_question}\nSQL Query: {corrected_sql_query}\nGenerate a suitable explanation for this query."
            response = invoke_openai_response(response_prompt)
            st.write("Generated SQL Query:")
            st.code(corrected_sql_query)
            if not df.empty:
                st.dataframe(df)
                graph_type = determine_graph_type(user_question)
                if 'listing_state' in df.columns and 'revenue_difference' in df.columns:
                    create_plotly_graph(df, graph_type, "listing_state", "revenue_difference", "Total Revenue Difference by Listing State")

st.write("Example Queries:")
st.write("What is the total revenue by listing state?")
st.write("Which are the top 10 SKUs by total profit?")
st.write("Can you show me the quarterly revenue trend?")
st.write("What are the top 5 ASINs by total ordered items?")
st.write("Can you create a graph that shows the difference in revenue by listing state?")
