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
