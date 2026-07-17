from fastapi import FastAPI, Request
import httpx
import uvicorn

app = FastAPI()

# Your WhatsApp credentials
PHONE_NUMBER_ID = "1264497586738434"
ACCESS_TOKEN = "EAAteYc0hvJEBR8s8cCbTTtyrcxTzyblgoeUtCevizwHzuBOwf4XNIH3EoqDIZAT2RrQCS276jUaEsLqyeJ8ow9d14XtNAwSZCK47LY6KUSjniRD4opebvzEOCkveje6TiTdxc5xJP4xd01w469bZCoFDVtfOCKw3VwY8ypZBC2uxM2fJw5qATSpq85CZCbjFGQruM0xCqHaSZCoB50vY9ZAYJWbxG2Rk9crxYkuTQEEJL7wl2XvmYRmSNnX4pSDOPFt02XNBLdZAi3vFMB2xmfM2czL5ZBKeapZBNZCHQZDZD"
VERIFY_TOKEN = "rahulbot123"

# Webhook verification — WhatsApp checks this first!!
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

# Receive WhatsApp messages!!
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
                # Send reply back!!
                await send_whatsapp_message(from_number, f"Hello!! You said: {customer_message}")
    except Exception as e:
        print(f"Error: {e}")
    return {"status": "ok"}

# Send WhatsApp message function!!
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
    import os
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))