import json

import requests


body = {
    "city": "Moscow",
    "street": "Lenina",
    "house": 1,
    "user_id": 1
}

url = "http://127.0.0.1:8000/addrs/"

result = requests.post(url=url, data=json.dumps(body))
print(result.status_code, result.text)