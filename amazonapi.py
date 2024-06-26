import requests

# Define the endpoint and headers
url = "https://real-time-amazon-data.p.rapidapi.com/seller-products"
headers = {
    "Content-Type": "application/json",
    "X-RapidAPI-Key": "4b717a92f9msh0b0e11879f156edp1a9798jsn699284b1432e",
    "X-RapidAPI-Host": "real-time-amazon-data.p.rapidapi.com"
}

# Define the query parameters
querystring = {"seller_id": "A02211013Q5HP3OMSZC7W", "country": "US", "page": "1"}

# Make the GET request
response = requests.get(url, headers=headers, params=querystring)

# Check if the request was successful
if response.status_code == 200:
    data = response.json()
    print("Data retrieved successfully")
    print(data)
else:
    print(f"Failed to retrieve data: {response.status_code}")
    print(response.json())
