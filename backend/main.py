# backend/main.py
import os

os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"

# from fastapi import FastAPI, Form, HTTPException
# from fastapi.middleware.cors import CORSMiddleware
# from fastapi.responses import HTMLResponse, FileResponse
# from pathlib import Path
# from models.schemas import RecognitionResponse, RegistrationResponse
# from services.face_processor import register_face, recognize_face
# import cv2
# import numpy as np
# import base64


from fastapi import FastAPI, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, FileResponse
from pathlib import Path

from models.schemas import RecognitionResponse, RegistrationResponse
from services.face_processor import register_face, recognize_face

import numpy as np
import base64


app = FastAPI(title="Face Lock API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Resolve frontend path relative to this file
FRONTEND_DIR = Path(__file__).  parent.parent / "frontend"

if not FRONTEND_DIR.exists():
    raise RuntimeError(f"Frontend directory not found at: {FRONTEND_DIR}")

# ✅ Serve root: /
@app.get("/", response_class=HTMLResponse)
async def root():
    return FileResponse(FRONTEND_DIR / "index.html")

# ✅ Serve other static files explicitly
@app.get("/register.html", response_class=HTMLResponse)
async def register_page():
    return FileResponse(FRONTEND_DIR / "register.html")

@app.get("/detect.html", response_class=HTMLResponse)
async def detect_page():
    return FileResponse(FRONTEND_DIR / "detect.html")

@app.get("/style.css")
async def style_css():
    return FileResponse(FRONTEND_DIR / "style.css")

@app.get("/script.js")
async def script_js():
    return FileResponse(FRONTEND_DIR / "script.js")

# ✅ API Endpoints
# In your /register and /recognize endpoints:


@app.post("/register", response_model=RegistrationResponse)
async def register(name: str = Form(...), frame: str = Form(...)):
    try:
        # ✅ frame is PURE base64 (no "image/..." prefix)
        image_data = base64.b64decode(frame)  # ← No split needed!
        nparr = np.frombuffer(image_data, np.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        if image is None:
            raise ValueError("Invalid image")
    except Exception:
        raise HTTPException(400, "Invalid image data")

    if not register_face(name, image):
        raise HTTPException(400, "Face already registered or no face detected.")

    return {"message": f"Face registered for {name}"}


@app.post("/recognize", response_model=RecognitionResponse)
async def recognize(frame: str = Form(...)):
# For register
    try:
        nparr = np.frombuffer(base64.b64decode(frame), np.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        if image is None:
            raise ValueError("Invalid image")
    except Exception:
        raise HTTPException(400, "Invalid image data")

    # For register
    try:
        nparr = np.frombuffer(base64.b64decode(frame), np.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        if image is None:
            raise ValueError("Invalid image")
    except Exception:
        raise HTTPException(400, "Invalid image data")

    name, confidence = recognize_face(image)
    return {"name": name, "confidence": round(confidence, 2)}


from fastapi import FastAPI

app = FastAPI()

