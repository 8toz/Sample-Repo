import requests

r = requests.get("https://google.es")
print(r.status_code)
print(r.ok)