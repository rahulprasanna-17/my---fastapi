from fastapi import FastAPI, Request
import httpx
import uvicorn
import os

app = FastAPI()

# WhatsApp credentials
PHONE_NUMBER_ID = os.environ.get("PHONE_NUMBER_ID", "1264497586738434")
ACCESS_TOKEN = os.environ.get("ACCESS_TOKEN", "your_permanent_token_here")
VERIFY_TOKEN = os.environ.get("VERIFY_TOKEN", "rahulbot123")
CLAUDE_API_KEY = os.environ.get("CLAUDE_API_KEY", "")

# Webhook verification
@app.get("/webhook")
async def verify_webhook(request: Request):
    params = dict(request.query_params)
    mode = params.get("hub.mode")
    token = params.get("hub.verify_token")
    challenge = params.get("hub.challenge")
    if mode == "subscribe" and token == VERIFY_TOKEN:
        print("Webhook verified!!")
        return int(challenge)
    return {"status": "verification failed"}

# Receive WhatsApp messages
@app.post("/webhook")
async def receive_message(request: Request):
    data = await request.json()
    print(f"Received: {data}")
    try:
        entry = data["entry"][0]
        changes = entry["changes"][0]
        value = changes["value"]
        if "messages" in value:
            message = value["messages"][0]
            from_number = message["from"]
            if message["type"] == "text":
                customer_message = message["text"]["body"]
                print(f"Message from {from_number}: {customer_message}")
                # Get Claude AI reply
                claude_reply = await ask_claude(customer_message)
                # Send reply back
                await send_whatsapp_message(from_number, claude_reply)
    except Exception as e:
        print(f"Error: {e}")
    return {"status": "ok"}

# Ask Claude AI
async def ask_claude(message: str):
    if not CLAUDE_API_KEY:
        return "Hello!! I am WorldOfBots assistant!! Claude AI coming soon!!"
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://api.anthropic.com/v1/messages",
                headers={
                    "x-api-key": CLAUDE_API_KEY,
                    "anthropic-version": "2023-06-01",
                    "content-type": "application/json"
                },
                json={
                    "model": "claude-sonnet-4-6",
                    "max_tokens": 1000,
                    "system": "You are a helpful WhatsApp customer service assistant for WorldOfBots. Be friendly, helpful and concise in your replies!!",
                    "messages": [
                        {"role": "user", "content": message}
                    ]
                },
                timeout=30.0
            )
            data = response.json()
            return data["content"][0]["text"]
    except Exception as e:
        print(f"Claude error: {e}")
        return "Sorry!! I am having trouble right now!! Please try again!!"

# Send WhatsApp message
async def send_whatsapp_message(to_number: str, message: str):
    url = f"https://graph.facebook.com/v25.0/{PHONE_NUMBER_ID}/messages"
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    data = {
        "messaging_product": "whatsapp",
        "to": to_number,
        "type": "text",
        "text": {"body": message}
    }
    async with httpx.AsyncClient() as client:
        response = await client.post(url, headers=headers, json=data)
        print(f"Message sent: {response.status_code}")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)
