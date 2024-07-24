import openai
from dotenv import load_dotenv
import os

# Load the environment variables from .env
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    raise ValueError("The OPENAI_API_KEY environment variable is not set.")

# Create a client instance with the API key
client = openai.OpenAI(
    api_key=OPENAI_API_KEY
)

def invoke_openai_sql(prompt):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant, who is an expert on a given database."},
            {"role": "user", "content": prompt}
        ]
    )
    message_content = response.choices[0].message.content.strip()
    sql_query_start = message_content.find("SELECT")
    sql_query = message_content[sql_query_start:]
    return sql_query

def invoke_openai_response(prompt):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
    )
    answer = response.choices[0].message.content.strip()
    return answer


def validate_sql_columns(sql_query, valid_columns):
    sql_keywords = {'SELECT', 'AS', 'FROM', 'WHERE', 'GROUP', 'BY', 'ORDER', 'DESC', 'LIMIT', 'SUM', 'AVG', 'COUNT', 'WITH', 'LEFT', 'JOIN', 'ON', 'COALESCE', 'WITH'}
    sql_query_columns = [word.strip('`,') for word in sql_query.split() if word.strip('`,').isalpha() and word.upper() not in sql_keywords]

    corrected_query = sql_query
    for col in sql_query_columns:
        if col.lower() not in [vc.lower() for vc in valid_columns]:
            corrected_query = corrected_query.replace(col, get_correct_column_name(col, valid_columns))

    return corrected_query

def get_correct_column_name(column, valid_columns):
    # Function to get the correct column name (e.g., handle typos or suggest corrections)
    for valid_col in valid_columns:
        if valid_col.lower() == column.lower():
            return valid_col
    return column  