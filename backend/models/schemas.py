from pydantic import BaseModel

class RegistrationResponse(BaseModel):
    message: str

class RecognitionResponse(BaseModel):
    name: str
    confidence: float