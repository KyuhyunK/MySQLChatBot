from transformers import AutoModelForCausalLM, AutoTokenizer

model_path = "C:/Users/SamuelCho/Desktop/Llama"  # Replace with actual model path
print(f"Loading model from: {model_path}")

try:
    tokenizer = AutoTokenizer.from_pretrained(model_path)
    model = AutoModelForCausalLM.from_pretrained(model_path)
    print("Model and tokenizer loaded successfully.")
except Exception as e:
    print(f"Error: {e}")
