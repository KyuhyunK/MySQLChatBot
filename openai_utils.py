import openai
from config import OPENAI_API_KEY

if not OPENAI_API_KEY:
    raise ValueError("The OPENAI_API_KEY environment variable is not set.")

# Create a client instance
client = openai.Client(api_key=OPENAI_API_KEY)
openai.api_key = OPENAI_API_KEY


def invoke_openai_sql(prompt):
    response = client.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant, who is an expert on a given database."},
            {"role": "user", "content": prompt}
        ]
    )
    message_content = response['choices'][0]['message']['content'].strip()
    sql_query_start = message_content.find("SELECT")
    sql_query = message_content[sql_query_start:]
    return sql_query

def invoke_openai_response(prompt):
    response = client.Chatompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
    )
    answer = response['choices'][0]['message']['content'].strip()
    return answer

def validate_sql_columns(sql_query, valid_columns):
    sql_keywords = {'SELECT', 'AS', 'FROM', 'WHERE', 'GROUP', 'BY', 'ORDER', 'DESC', 'LIMIT', 'SUM', 'AVG', 'COUNT'}
    sql_query_columns = [word.strip('`,') for word in sql_query.split() if word.strip('`,').isalpha() and word.upper() not in sql_keywords]
    invalid_columns = [col for col in sql_query_columns if col.lower() not in [col.lower() for col in valid_columns]]
    corrected_query = sql_query
    for invalid_col in invalid_columns:
        if invalid_col == 'revenue':
            corrected_query = corrected_query.replace('revenue', 'total_revenue')
        # Add more replacements if necessary
    return corrected_query
