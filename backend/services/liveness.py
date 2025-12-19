import cv2
import dlib
import numpy as np

# Initialize dlib's face detector and landmark predictor
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")  # ← Download this!

def eye_aspect_ratio(eye):
    A = np.linalg.norm(eye[1] - eye[5])
    B = np.linalg.norm(eye[2] - eye[4])
    C = np.linalg.norm(eye[0] - eye[3])
    return (A + B) / (2.0 * C)

def is_blink_detected(frame, threshold=0.25, consecutive_frames=2):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = detector(gray)
    if len(faces) != 1:
        return False  # Require exactly one face

    face = faces[0]
    landmarks = predictor(gray, face)
    left_eye = np.array([(landmarks.part(i).x, landmarks.part(i).y) for i in range(36, 42)])
    right_eye = np.array([(landmarks.part(i).x, landmarks.part(i).y) for i in range(42, 48)])

    ear_left = eye_aspect_ratio(left_eye)
    ear_right = eye_aspect_ratio(right_eye)
    ear = (ear_left + ear_right) / 2.0

    return ear < threshold  # Blink = eyes closed → low EAR