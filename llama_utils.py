# llama_utils.py
import transformers
from transformers import AutoModelForCausalLM, AutoTokenizer
# amazonapi.py or main.py
from llama_utils import load_llama_model, generate_llama_response
from config import LLAMA_MODEL_PATH


def load_llama_model(model_path):
    tokenizer = AutoTokenizer.from_pretrained(model_path)
    model = AutoModelForCausalLM.from_pretrained(model_path)
    return tokenizer, model

def generate_llama_response(prompt, tokenizer, model):
    inputs = tokenizer(prompt, return_tensors="pt")
    outputs = model.generate(**inputs)
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return response


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



# Load Llama model once during the initialization
tokenizer, model = load_llama_model(LLAMA_MODEL_PATH)

def invoke_chain(user_question, valid_columns):
    sql_query_prompt = f"Generate a SQL query for the following question: {user_question}. The default table name is 'aggregate_profit_data', unless specified otherwise use this table name. Ensure the query includes the table name and the 'FROM' keyword. Use only valid columns from the following list: {', '.join(valid_columns)}. Keep your response concise and easy to understand."
    
    generated_sql_query = generate_llama_response(sql_query_prompt, tokenizer, model)
    print("Generated SQL Query:", generated_sql_query)

    corrected_sql_query = validate_sql_columns(generated_sql_query, valid_columns)
    return corrected_sql_query
