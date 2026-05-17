import os
import uuid
import subprocess
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from typing import Optional

from backend.audio_utils import extract_audio, speech_to_text
from backend.text_model import detect_bullying
from backend.word_manager import load_word_dicts
from backend.severity_engine import (
    calculate_severity_and_confidence,
    extract_matched_words
)

from backend.prediction_engine import predict_unseen_words

from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix


TMP_DIR = "tmp_media"
os.makedirs(TMP_DIR, exist_ok=True)


# File Verification

def is_audio_file(name):
    return name.lower().endswith((".mp3",".wav",".m4a",".aac"))


def is_video_file(name):
    return name.lower().endswith((".mp4",".mov",".mkv",".avi"))


def is_dataset_file(name):
    return name.lower().endswith((".csv",".xlsx"))


# Text analysis pipeline

def analyze_text_pipeline(text, allow_prediction=False):

    text = text.lower().strip()

    offensive_dict, explicit_dict = load_word_dicts()

    offensive_matches = extract_matched_words(text, offensive_dict, "offensive")
    explicit_matches = extract_matched_words(text, explicit_dict, "explicit")

    matches = offensive_matches + explicit_matches

    offensive_words = [m["word"] for m in offensive_matches]
    explicit_words = [m["word"] for m in explicit_matches]

    model_label, model_score = detect_bullying(text)

    severity, confidence, trigger_word = calculate_severity_and_confidence(matches)

    if not matches:
        severity = 0
        confidence = 0
        trigger_word = None

    predicted_words = []

    if allow_prediction:
        predicted_words = predict_unseen_words(text)

    return {

        "text": text,
        "label": model_label,

        "severity": severity,
        "confidence": confidence,
        "trigger_word": trigger_word,

        "matched_offensive_words": offensive_words,
        "matched_explicit_words": explicit_words,

    }


# Evaluation of Dataset

def evaluate_dataset(path):

    try:

        if path.endswith(".csv"):
            df = pd.read_csv(path)
        else:
            df = pd.read_excel(path)

        if df.empty:
            return {"error": "Dataset empty"}

        if len(df) > 2000:
            df = df.sample(n=2000, random_state=42)

        # Text column detection (long string column)

        text_column = None

        for col in df.columns:

            if df[col].dtype == "object":

                avg_len = df[col].astype(str).str.len().mean()

                if avg_len > 20:
                    text_column = col
                    break

        if text_column is None:
            return {"error": "Text column not detected"}

        
        # Label Column Detection (few unique values)

        label_column = None

        for col in df.columns:

            unique_vals = df[col].nunique()

            if 1 < unique_vals <= 10:
                label_column = col

        if label_column is None:
            return {"error": "Label column not detected"}

       
        # Normalizing the variables

        def normalize_label(value):

            value = str(value).lower()

            toxic_values = [
                "1","true","yes","toxic",
                "hate","offensive",
                "cyberbullying","abusive",
                "insult","attack"
            ]

            if value in toxic_values:
                return "toxic"

            return "neutral"

        # Predition loop

        y_true = []
        y_pred = []

        for text, label in zip(df[text_column], df[label_column]):

            if pd.isna(text):
                continue

            result = analyze_text_pipeline(str(text))

            true_label = normalize_label(label)

            pred_label = result["label"].lower()

            if pred_label not in ["toxic", "neutral"]:
                pred_label = "toxic"

            y_true.append(true_label)
            y_pred.append(pred_label)

        # Metrics

        accuracy = accuracy_score(y_true, y_pred)

        precision = precision_score(
            y_true, y_pred,
            average="binary",
            pos_label="toxic",
            zero_division=0
        )

        recall = recall_score(
            y_true, y_pred,
            average="binary",
            pos_label="toxic",
            zero_division=0
        )

        f1 = f1_score(
            y_true, y_pred,
            average="binary",
            pos_label="toxic",
            zero_division=0
        )

        # Confusion Matrix

        labels = ["neutral", "toxic"]

        cm = confusion_matrix(
            y_true,
            y_pred,
            labels=labels
        )

        plt.figure(figsize=(6,5))

        sns.heatmap(
            cm,
            annot=True,
            fmt="d",
            cmap="Blues",
            xticklabels=labels,
            yticklabels=labels
        )

        plt.title("Confusion Matrix")
        plt.xlabel("Predicted")
        plt.ylabel("Actual")

        # prevent file overwrite
        filename = f"confusion_matrix_{uuid.uuid4().hex}.png"

        heatmap_path = os.path.join(TMP_DIR, filename)

        plt.savefig(heatmap_path)
        plt.close()

        return {

            "mode": "dataset_evaluation",

            "accuracy": round(float(accuracy),4),
            "precision": round(float(precision),4),
            "recall": round(float(recall),4),
            "f1_score": round(float(f1),4),

            "confusion_matrix": cm.tolist(),
            "heatmap_file": heatmap_path
        }

    except Exception as e:

        return {"error": str(e)}

# Main inout proessor

def process_input(file: Optional[object], url: Optional[str], text: Optional[str]):

    temp_file = None
    temp_audio = None

    try:

        uid = uuid.uuid4().hex

        if text and text.strip():
            return analyze_text_pipeline(text)

        if file:

            filename = file.filename.replace(" ","_")

            temp_file = os.path.join(TMP_DIR,f"{uid}_{filename}")

            with open(temp_file,"wb") as f:
                while chunk := file.file.read(1024*1024):
                    f.write(chunk)

        elif url:

            temp_audio = os.path.join(TMP_DIR,f"url_audio_{uid}.wav")

            command = [
                "yt-dlp",
                "-f","bestaudio",
                "--extract-audio",
                "--audio-format","wav",
                "-o",temp_audio,
                url
            ]

            subprocess.run(command)

            speech = speech_to_text(temp_audio)

            if not speech:
                return {"error":"No speech detected"}

            # URL MODE → disable prediction
            return analyze_text_pipeline(speech, allow_prediction=False)

        if is_dataset_file(temp_file):
            return evaluate_dataset(temp_file)

        if is_audio_file(temp_file):

            speech = speech_to_text(temp_file)
            return analyze_text_pipeline(speech)

        if is_video_file(temp_file):

            temp_audio = extract_audio(temp_file)
            speech = speech_to_text(temp_audio)

            return analyze_text_pipeline(speech)

        return {"error":"Unsupported input type"}

    finally:

        try:

            if temp_audio and os.path.exists(temp_audio):
                os.remove(temp_audio)

            if temp_file and os.path.exists(temp_file):
                os.remove(temp_file)

        except:
            pass