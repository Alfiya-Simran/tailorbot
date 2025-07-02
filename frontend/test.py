import requests

response = requests.post(
    "http://127.0.0.1:8000/chat",
    json={"message": "Hello"}
)

print("Status Code:", response.status_code)
print("Response:", response.text)
