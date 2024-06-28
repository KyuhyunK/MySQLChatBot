import streamlit as st
import plotly.express as px
from database import get_table_columns, run_query
from intents import intents, valid_columns
import requests
from t5_utils import load_model, generate__response, validate_sql_columns
from config import MODEL_NAME
import torch
import logging


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

model = None
tokenizer = None

@st.cache(allow_output_mutation=True)
def load_model():
    model_name = "google/flan-t5-base"
    try:
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
        return tokenizer, model
    except Exception as e:
        st.error(f"Error loading model or tokenizer: {e}")
        return None, None


tokenizer, model = get_model()

def invoke_chain(user_question, valid_columns):
    # Prepare the prompt for generating the SQL query
    sql_query_prompt = f"Generate a SQL query for the following question: {user_question}. The default table name is 'aggregate_profit_data', unless specified otherwise use this table name. Ensure the query includes the table name and the 'FROM' keyword. Use only valid columns from the following list: {', '.join(valid_columns)}. Keep your response concise and easy to understand."
    
    # Use the model to generate the SQL query
    generated_sql_query = generate_response(sql_query_prompt, tokenizer, model)
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

# Streamlit application code
def main():
    st.title('AI Chat Interface for MySQL Database')

    st.write("Welcome to the AI Chat Interface for MySQL Database. You can ask questions about the database, and I will help you retrieve and visualize the data.\n") 

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
                response = generate_response(f"Endpoint: {endpoint}, Params: {params}", tokenizer, model)
                st.write("Model Response:")
                st.json(response)
            else:
                corrected_sql_query = invoke_chain(user_question, valid_columns=[])
                df, result = run_query(corrected_sql_query)
                response_prompt = f"User question: {user_question}\nSQL Query: {corrected_sql_query}\nGenerate a suitable explanation for this query."
                response = generate_response(response_prompt, tokenizer, model)
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
