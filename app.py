import os
from fastapi import FastAPI, Request, HTTPException

from utils.webhook_validator import verify_webhook
from utils.http_client import HttpClient
from utils.logger import setup_logger
from automation.message_router import route_message
from automation.response_builder import build_response

app = FastAPI()
logger = setup_logger()

VERIFY_TOKEN = os.getenv("VERIFY_TOKEN", "CHANGE_ME")
PAGE_ACCESS_TOKEN = os.getenv("PAGE_ACCESS_TOKEN", "")
GRAPH_API_BASE = os.getenv("GRAPH_API_BASE", "https://graph.facebook.com/v19.0")

client = HttpClient()

@app.get("/webhook")
def webhook_verify(hub_mode: str, hub_verify_token: str, hub_challenge: str):
    result = verify_webhook(hub_mode, hub_verify_token, hub_challenge, VERIFY_TOKEN)
    if result:
        return int(result)
    raise HTTPException(status_code=403, detail="Verification failed")

@app.post("/webhook")
async def webhook(request: Request):
    payload = await request.json()
    try:
        entry = payload["entry"][0]["messaging"][0]
        sender_id = entry["sender"]["id"]
        text = entry.get("message", {}).get("text", "")

        route = route_message(text)
        reply = build_response(route)

        url = f"{GRAPH_API_BASE}/me/messages"
        headers = {
            "Authorization": f"Bearer {PAGE_ACCESS_TOKEN}",
            "Content-Type": "application/json"
        }
        body = {
            "recipient": {"id": sender_id},
            "message": {"text": reply}
        }
        client.post(url, headers=headers, json=body)
        logger.info(f"Replied to {sender_id}: {reply}")
    except Exception as e:
        logger.error(str(e))
    return {"status": "ok"}
