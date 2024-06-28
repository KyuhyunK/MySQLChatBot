from transformers import T5Tokenizer, T5ForConditionalGeneration
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

def load_model(model_path):
    print(f"Loading model from: {model_path}")
    try:
        self.tokenizer = T5Tokenizer.from_pretrained(tokenizer_name)
        self.model = T5ForConditionalGeneration.from_pretrained(model_name)
        print("Model and tokenizer loaded successfully.")
    except Exception as e:
        print(f"Error: {e}")
        tokenizer = None
        model = None
    return tokenizer, model

def generate_response(prompt, tokenizer, model):
    if tokenizer is None or model is None:
        return "Error: Model or tokenizer not loaded properly."
    try:
        inputs = tokenizer(prompt, return_tensors="pt")
        outputs = model.generate(**inputs)
        decoded_output = tokenizer.decode(outputs[0], skip_special_tokens=True)
        return decoded_output
    except Exception as e:
        return f"Error generating response: {e}"


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
