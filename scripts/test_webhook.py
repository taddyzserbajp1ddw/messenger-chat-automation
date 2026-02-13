import requests

payload = {
  "entry": [{
    "messaging": [{
      "sender": {"id": "123456"},
      "message": {"text": "hi"}
    }]
  }]
}

r = requests.post("http://localhost:8000/webhook", json=payload)
print(r.json())
