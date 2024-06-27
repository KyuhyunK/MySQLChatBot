import streamlit as st
import plotly.express as px
from database import get_table_columns, run_query
from intents import intents, valid_columns
import requests
from llama_utils import load_llama_model, generate_llama_response, validate_sql_columns
from config import LLAMA_MODEL_PATH


@st.cache_resource
def get_model():
    print(f"Using model path: {LLAMA_MODEL_PATH}")
    return load_llama_model(LLAMA_MODEL_PATH)

tokenizer, model = get_model()

def invoke_chain(user_question, valid_columns):
    # Prepare the prompt for generating the SQL query
    sql_query_prompt = f"Generate a SQL query for the following question: {user_question}. The default table name is 'aggregate_profit_data', unless specified otherwise use this table name. Ensure the query includes the table name and the 'FROM' keyword. Use only valid columns from the following list: {', '.join(valid_columns)}. Keep your response concise and easy to understand."
    
    # Use the Llama model to generate the SQL query
    generated_sql_query = generate_llama_response(sql_query_prompt, tokenizer, model)
    print("Generated SQL Query:", generated_sql_query)

    # Validate and correct the SQL query if needed
    corrected_sql_query = validate_sql_columns(generated_sql_query, valid_columns)

    return corrected_sql_query

# Graph structure
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
            data = invoke_amazon_api(endpoint, params)
            st.write("Amazon API Response:")
            st.json(data)
            # Additional processing and visualization if needed
        else:
            corrected_sql_query = invoke_chain(user_question, valid_columns)
            df, result = run_query(corrected_sql_query)
            response_prompt = f"User question: {user_question}\nSQL Query: {corrected_sql_query}\nGenerate a suitable explanation for this query."
            response = invoke_amazon_response(response_prompt)
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
