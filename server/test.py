import requests

BASE = "http://127.0.0.1:5000/"

response = requests.get(BASE + "mmr/1d2192dd-a26a-5989-bbf4-f770cb73785b")
print(response.json())