from dotenv import load_dotenv
import os 
import requests

load_dotenv()

webhook = os.getenv("DISCORD_WEBHOOK")

def SEND_AUDIT_LOG(message,urgency): # Urgency can be "True" or "False", true for when pinging @eveyrone, false for normal messages
    ret = "@everyone\n" if urgency else ""
    ret += message

    message_data = {
        "content": ret,
    }

    try:
        response = requests.post(webhook, json=message_data)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Error sending webhook: {e}")