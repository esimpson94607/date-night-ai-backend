from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ReminderPayload(BaseModel):
    to_email: str
    date: str
    itinerary: str

@app.post("/send-email-reminder")
def send_email_reminder(payload: ReminderPayload):
    try:
        body = {
            "from": "Date Night App <reminder@datenightapp.ai>",
            "to": [payload.to_email],
            "subject": "Your Date Night is Coming Up! ❤️",
            "html": f"""
                <h2>Your date night starts soon!</h2>
                <p><strong>When:</strong> {payload.date}</p>
                <p><strong>Plan:</strong><br>{payload.itinerary.replace("\n", "<br>")}</p>
                <p>Enjoy your evening! 💑</p>
            """
        }

        res = requests.post(
            "https://api.resend.com/emails",
            headers={
                "Authorization": f"Bearer {os.getenv('RESEND_API_KEY')}",
                "Content-Type": "application/json"
            },
            json=body
        )

        if res.status_code == 200:
            return { "status": "sent" }
        else:
            return { "status": "failed", "details": res.text }

    except Exception as e:
        return { "error": str(e) }