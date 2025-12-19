import os
import cv2
import numpy as np
from deepface import DeepFace

# Use OpenCV for face detection
FACE_CASCADE = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

STORAGE_DIR = "backend/storage/registered_faces"
os.makedirs(STORAGE_DIR, exist_ok=True)

def extract_face(image: np.ndarray):
    """Extract the largest face from the image."""
    try:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        faces = FACE_CASCADE.detectMultiScale(gray, 1.1, 3, minSize=(60, 60))
        if len(faces) == 0:
            return None
        # Get the largest face
        faces = sorted(faces, key=lambda x: x[2] * x[3], reverse=True)
        x, y, w, h = faces[0]
        return image[y:y+h, x:x+w]
    except:
        return None

def register_face(name: str, image: np.ndarray) -> bool:
    try:
        # Check if face exists
        faces = DeepFace.extract_faces(
            img_path=image,
            detector_backend="opencv",
            enforce_detection=False
        )
        if not faces:
            return False

        # Check for duplicates
        for filename in os.listdir(STORAGE_DIR):
            if not filename.lower().endswith(('.png', '.jpg', '.jpeg')):
                continue
            stored_path = os.path.join(STORAGE_DIR, filename)
            try:
                result = DeepFace.verify(
                    img1_path=image,
                    img2_path=stored_path,
                    model_name="Facenet",
                    detector_backend="opencv",
                    enforce_detection=False,
                    silent=True
                )
                if result["verified"]:
                    return False  # Already registered
            except:
                continue

        # Save new face
        safe_name = "".join(c for c in name if c.isalnum() or c in (" ", "_")).rstrip()
        filepath = os.path.join(STORAGE_DIR, f"{safe_name}.jpg")
        cv2.imwrite(filepath, image)
        return True
    except:
        return False

def recognize_face(image: np.ndarray):
    """Recognize using cropped face."""
    face = extract_face(image)
    if face is None:
        return "Unknown", 0.0

    if not os.listdir(STORAGE_DIR):
        return "Unknown", 0.0

    best_match = "Unknown"
    best_conf = 0.0

    for filename in os.listdir(STORAGE_DIR):
        if not filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            continue
        stored_path = os.path.join(STORAGE_DIR, filename)
        name = os.path.splitext(filename)[0]
        try:
            result = DeepFace.verify(
                img1_path=face,
                img2_path=stored_path,
                model_name="Facenet",
                detector_backend="opencv",
                enforce_detection=False,
                silent=True
            )
            if result["verified"]:
                conf = 1.0 - result["distance"]
                if conf > best_conf:
                    best_conf = conf
                    best_match = name
        except Exception as e:
            print(f"⚠️ Verification error: {e}")
            continue

    return (best_match, best_conf) if best_conf > 0.4 else ("Unknown", 0.0)