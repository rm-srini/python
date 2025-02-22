import requests
url = 'http://localhost:8000/greet?name=Srini'
response = requests.get(url)
print(response.json())