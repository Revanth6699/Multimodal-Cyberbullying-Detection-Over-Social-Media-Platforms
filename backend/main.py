from fastapi import FastAPI, UploadFile, File, Form
from typing import Optional
import os
import json
from datetime import datetime

from backend.input_handler import process_input
from backend.word_manager import add_word, delete_word

app = FastAPI(title="Cyberbullying Detection API")

LOG_FILE = "data/logs.json"


# Logging Function

def log_prediction(result):

    try:

        if not isinstance(result, dict):
            return

        if "text" not in result:
            return

        os.makedirs("data", exist_ok=True)

        log_entry = {
            "timestamp": str(datetime.now()),
            "text": result.get("text"),
            "label": result.get("label"),
            "severity": result.get("severity"),
            "trigger_word": result.get("trigger_word")
        }

        if os.path.exists(LOG_FILE):

            with open(LOG_FILE, "r") as f:
                try:
                    logs = json.load(f)
                except:
                    logs = []

        else:
            logs = []

        logs.append(log_entry)

        with open(LOG_FILE, "w") as f:
            json.dump(logs, f, indent=2)

    except Exception:
        pass


# Root

@app.get("/")
def home():

    return {
        "message": "Cyberbullying Detection API running"
    }


# Analyze Endpoint

@app.post("/analyze")
async def analyze(
    file: Optional[UploadFile] = File(None),
    url: Optional[str] = Form(None),
    text: Optional[str] = Form(None)
):

    try:

        # Swagger default placeholder fix
        if text == "string":
            text = None

        if url == "string":
            url = None

        # Only one input allowed
        inputs = sum([
            file is not None,
            bool(url),
            bool(text)
        ])

        if inputs == 0:
            return {"error": "Provide file OR url OR text"}

        if inputs > 1:
            return {"error": "Provide only one input at a time"}

        result = process_input(file=file, url=url, text=text)

        if isinstance(result, dict) and "text" in result:
            log_prediction(result)

        return result

    except Exception as e:

        return {
            "error": "Input processing failed",
            "reason": str(e)
        }


# ADD Word (manual)

@app.post("/add_word")
def add_word_api(
    word: str = Form(...),
    category: str = Form(...),   # offensive or explicit
    severity: int = Form(2)
):

    try:

        word = word.lower().strip()

        if category not in ["offensive", "explicit"]:
            return {"error": "category must be 'offensive' or 'explicit'"}

        result = add_word(word, category, severity)

        return result

    except Exception as e:

        return {"error": str(e)}


# DELETE Word (remove from both files)

@app.post("/delete_word")
def delete_word_api(
    word: str = Form(...)
):

    try:

        word = word.lower().strip()

        result = delete_word(word)

        return result

    except Exception as e:

        return {"error": str(e)}