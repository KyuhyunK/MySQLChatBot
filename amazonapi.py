import requests
import json
from config import RAPIDAPI_KEY

def get_amazon_data(endpoint, params):
    url = f"https://real-time-amazon-data.p.rapidapi.com/{endpoint}"
    headers = {
        'x-rapidapi-host': 'real-time-amazon-data.p.rapidapi.com',
        'x-rapidapi-key': RAPIDAPI_KEY,
        'Content-Type': 'application/json'
    }
    response = requests.get(url, headers=headers, params=params)
    return response.json()

# Example usage
if __name__ == "__main__":
    endpoint = "seller-products"
    params = {
        "seller_id": "A02211013Q5HP3OMSZC7W",
        "country": "US",
        "page": "1"
    }
    data = get_amazon_data(endpoint, params)
    print(json.dumps(data, indent=4))
