import os

import requests
from dotenv import load_dotenv

load_dotenv()

BREVO_API_URL = "https://api.brevo.com/v3/smtp/email"
BREVO_API_KEY = os.environ.get("BREVO_API_KEY")
SENDER_EMAIL = os.environ.get("BREVO_SENDER_EMAIL")
SENDER_NAME = "CrashAlert System"

RECIPIENTS = [
    {"email": "khanalaashraya1@gmail.com", "Aashraya Khanal": "Teammate 1"},
    {"email": "nabinpoudel369@gmail.com", "Nabin Paudel": "Teammate 2"},
    {"email": "shahgaurav2378@gmail.com", "Gaurav Shah": "Teammate 3"},
]


def send_alert_email(camera_id: str, location: str, severity: str, maps_url: str = None) -> dict:
    if not BREVO_API_KEY or not SENDER_EMAIL:
        print("BREVO_API_KEY or BREVO_SENDER_EMAIL not set, skipping email send.")
        return {"email_sent": False, "reason": "Email not configured"}

    subject = f"CrashAlert: Accident Detected — {location} (Severity {severity})"
    map_line = f'<p><a href="{maps_url}">📍 View Location</a></p>' if maps_url else ""

    html_content = f"""
    <h2>CrashAlert - Accident Detected</h2>
    <p><strong>Camera:</strong> {camera_id}</p>
    <p><strong>Location:</strong> {location}</p>
    <p><strong>Severity:</strong> Level {severity}</p>
    {map_line}
    <p style="color:gray; font-size:12px;">
        This is a demo alert from the CrashAlert prototype, sent to project
        team members only — not a real emergency dispatch.
    </p>
    """

    payload = {
        "sender": {"name": SENDER_NAME, "email": SENDER_EMAIL},
        "to": RECIPIENTS,
        "subject": subject,
        "htmlContent": html_content,
    }
    headers = {
        "accept": "application/json",
        "api-key": BREVO_API_KEY,
        "content-type": "application/json",
    }

    try:
        response = requests.post(BREVO_API_URL, json=payload, headers=headers, timeout=10)
        response.raise_for_status()
        return {"email_sent": True}
    except requests.RequestException as e:
        print(f"Failed to send email via Brevo: {e}")
        return {"email_sent": False, "reason": str(e)}
