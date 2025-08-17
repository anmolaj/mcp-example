from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import whisper
import os

# Define request schema
class FilePathRequest(BaseModel):
    file_path: str

app = FastAPI()
model = whisper.load_model("base")  # Choose 'tiny', 'base', 'small', etc.

@app.post("/transcribe")
def transcribe(request: FilePathRequest):
    print(request.file_path)
    if not os.path.isfile(request.file_path):
        raise HTTPException(status_code=404, detail="File not found.")
    try:
        result = model.transcribe(request.file_path)
        return {"text": result['text']}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))