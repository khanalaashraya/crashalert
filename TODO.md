# CrashAlert: Newbie Run Guide

This project is a small AI-powered accident detection app:
- a FastAPI backend loads two YOLO models and analyzes uploaded images
- a simple frontend lets a user choose a camera and upload an image
- if an accident is detected, the app can generate an alert and location link

## 1) Prerequisites

Install:
- Python 3.10+ (3.11 is a safe choice)
- Git
- A browser

Optional but recommended:
- a virtual environment
- VS Code terminal

## 2) Clone and open the project

```bash
cd /workspaces/crashalert
```

## 3) Create a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

If you are on Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

## 4) Install Python dependencies

From the repo root:

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

This installs:
- FastAPI
- Uvicorn
- Python multipart
- Ultralytics
- Pillow
- requests
- python-dotenv

## 5) Start the backend

From the repo root:

```bash
uvicorn app.app:app --reload --host 0.0.0.0 --port 8000
```

Expected behavior:
- the app loads the accident and severity models
- the terminal should show messages like "Loading models..." and "Models loaded, backend ready."

To confirm the backend is running:

```bash
curl http://127.0.0.1:8000/
```

You should get a JSON response similar to:

```json
{"status": "CrashAlert backend is running"}
```

## 6) Start the frontend

Open a second terminal, then run:

```bash
cd /workspaces/crashalert/frontend
python -m http.server 8080
```

Then open this in your browser:

```text
http://localhost:8080
```

The page loads the UI and sends requests to the backend at:

```text
http://127.0.0.1:8000/analyze
```

## 7) Use the app

On the page:
1. Pick a camera ID from the dropdown (for example `CAM-01`)
2. Choose an image file to upload
3. Click "Analyze Frame"
4. Wait for the model to classify the image

The app expects camera values such as:
- `CAM-01`
- `CAM-02`
- `CAM-03`

## 8) Useful project paths

- Backend entry point: `app/app.py`
- Frontend files: `frontend/`
- Camera data: `location/camera_locations.py`
- Alert generation: `alerts/alerts_module.py`
- Model files: `model/`

## 9) Troubleshooting

### "No module named ..."
Run:

```bash
pip install -r requirements.txt
```

### Port 8000 already in use
Use another port:

```bash
uvicorn app.app:app --reload --host 0.0.0.0 --port 8001
```

Then update the frontend fetch URL in `frontend/script.js` if needed.

### Frontend shows "Backend Offline"
Make sure the backend is still running in the first terminal and that the URL is correct:

```text
http://127.0.0.1:8000/analyze
```

### Model load errors
Check that these files exist:

```bash
ls model/
```

You should see:
- `crashalert_accident_v2_model.pt`
- `crashalert_severity_v2_model.pt`

## 10) Typical run order for a beginner

```bash
cd /workspaces/crashalert
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
uvicorn app.app:app --reload --host 0.0.0.0 --port 8000
```

Then in another terminal:

```bash
cd /workspaces/crashalert/frontend
python -m http.server 8080
```

Then open:

```text
http://localhost:8080
```

That is the normal local workflow for this project.
