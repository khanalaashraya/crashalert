import io
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image
from ultralytics import YOLO

from location.camera_locations import get_location_name, get_coordinates, camera_exists
from alerts.alerts_module import generate_alert
from alerts.email_alert import send_alert_email
from alerts.phone_alert import send_alert_call

MODEL_DIR = PROJECT_ROOT / "model"
ACCIDENT_MODEL_PATH = MODEL_DIR / "crashalert_accident_v2_model.pt"
SEVERITY_MODEL_PATH = MODEL_DIR / "crashalert_severity_v2_model.pt"

app = FastAPI(title="CrashAlert Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

print("Loading models...")
accident_model = YOLO(str(ACCIDENT_MODEL_PATH))
severity_model = YOLO(str(SEVERITY_MODEL_PATH))
print("Models loaded, backend ready.")


@app.get("/")
def health_check():
    return {"status": "CrashAlert backend is running"}


@app.post("/analyze")
async def analyze(file: UploadFile = File(...), camera_id: str = Form(...)):
    if not camera_exists(camera_id):
        raise HTTPException(status_code=400, detail=f"Unknown camera_id: {camera_id}")

    image_bytes = await file.read()
    image = Image.open(io.BytesIO(image_bytes)).convert("RGB")

    result1 = accident_model.predict(source=image, verbose=False)[0]
    accident_class = result1.names[result1.probs.top1]
    accident_confidence = float(result1.probs.top1conf)
    is_accident = accident_class.strip().lower() == "accident"

    severity_class = None
    severity_confidence = None

    if is_accident:
        result2 = severity_model.predict(source=image, verbose=False)[0]
        severity_class = result2.names[result2.probs.top1]
        severity_confidence = float(result2.probs.top1conf)

    location = get_location_name(camera_id)
    coordinates = get_coordinates(camera_id)
    alert = generate_alert(is_accident, severity_class, location, camera_id, coordinates)

    email_result = {}
    call_result = {}
    if alert.get("alert_generated"):
        email_result = send_alert_email(
            camera_id=camera_id,
            location=location,
            severity=severity_class,
            maps_url=alert.get("maps_url"),
        )
        call_result = send_alert_call()

    return {
        "camera_id": camera_id,
        "location": location,
        "coordinates": coordinates,
        "accident": is_accident,
        "accident_confidence": accident_confidence,
        "severity": severity_class,
        "severity_confidence": severity_confidence,
        **alert,
        **email_result,
        **call_result,
    }
