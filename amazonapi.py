import requests
import json
from config import RAPIDAPI_KEY

def get_amazon_data(endpoint, params):
    url = f"https://real-time-amazon-data.p.rapidapi.com/{endpoint}"
    headers = {
        "X-RapidAPI-Key": RAPIDAPI_KEY,
        "X-RapidAPI-Host": "real-time-amazon-data.p.rapidapi.com"
    }
    response = requests.get(url, headers=headers, params=params)
    return response.json()




def invoke_amazon_api(endpoint, params):
    url = f"https://real-time-amazon-data.p.rapidapi.com/{endpoint}"
    headers = {
        "X-RapidAPI-Key": RAPIDAPI_KEY,
        "X-RapidAPI-Host": "real-time-amazon-data.p.rapidapi.com"
    }
    response = requests.get(url, headers=headers, params=params)
    data = response.json()
    return data

def invoke_amazon_response(prompt):
    endpoint = "endpoint_for_your_query"  # Specify the endpoint according to your API
    params = {"query": prompt}  # Set parameters for your API request
    data = invoke_amazon_api(endpoint, params)
    return data

def invoke_chain(user_question, valid_columns):
    sql_query_prompt = f"Generate a SQL query for the following question: {user_question}. The default table name is 'aggregate_profit_data', unless specified otherwise use this table name. Ensure the query includes the table name and the 'FROM' keyword. Use only valid columns from the following list: {', '.join(valid_columns)}. Keep your response concise and easy to understand."
    generated_sql_query = invoke_openai_sql(sql_query_prompt)
    print("Generated SQL Query:", generated_sql_query)

    corrected_sql_query = validate_sql_columns(generated_sql_query, valid_columns)

    return corrected_sql_query
