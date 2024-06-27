from transformers import AutoTokenizer, AutoModelForCausalLM
from huggingface_hub import login

# Login to Hugging Face with your token
huggingface_token = "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"  # Replace with your actual token
login(huggingface_token)

# Define the path where you want to save the model
model_path = "C:\\Users\\SamuelCho\\Desktop\\Llama"

# Define the model name
model_name = "meta-llama/Llama-2-7b-chat-hf"

# Download and save the tokenizer
tokenizer = AutoTokenizer.from_pretrained(model_name, use_auth_token=True)
tokenizer.save_pretrained(model_path)

# Download and save the model
model = AutoModelForCausalLM.from_pretrained(model_name, use_auth_token=True)
model.save_pretrained(model_path)
