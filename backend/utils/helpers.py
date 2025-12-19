import json
import os

def load_encodings(path: str):
    if not os.path.exists(path):
        return {}
    with open(path, "r") as f:
        return {name: list(enc) for name, enc in json.load(f).items()}

def save_encodings(data: dict, path: str):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        json.dump(data, f)