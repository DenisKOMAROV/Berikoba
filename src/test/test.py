import requests

# URL to make an HTTP GET request to
url = "http://127.0.0.1:8000/extra"

# Make the HTTP GET request
response = requests.get(url)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    data = response.json()  # Convert response to JSON format
    print("Response JSON:", data)
else:
    print("Request failed with status code:", response.status_code)