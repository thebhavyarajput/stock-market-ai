import requests
API_KEY = "3ab56217f71cc47203ea11d79000430f"
url = f"http://api.marketstack.com/v1/eod?access_key={API_KEY}&symbols=AAPL&date_from=2014-01-01&date_to=2024-10-01&limit=5"
response = requests.get(url)
print(response.json())
