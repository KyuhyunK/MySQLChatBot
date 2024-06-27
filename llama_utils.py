from transformers import AutoModelForCausalLM, AutoTokenizer
from huggingface_hub import login

def load_llama_model(model_path):
    print(f"Loading model from: {model_path}")
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
