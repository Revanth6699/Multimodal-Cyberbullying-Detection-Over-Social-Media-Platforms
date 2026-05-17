import os
import uuid
import subprocess
import whisper

# Whisper Model

model = whisper.load_model("base")


# extract audio from video

def extract_audio(video_path: str):

    try:

        audio_path = f"temp_audio_{uuid.uuid4().hex}.wav"

        command = [
            "ffmpeg",
            "-i", video_path,
            "-vn",
            "-acodec", "pcm_s16le",
            "-ar", "16000",
            "-ac", "1",
            audio_path,
            "-y"
        ]

        result = subprocess.run(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

        if result.returncode != 0:
            print("FFMPEG ERROR:", result.stderr.decode())
            return None

        if os.path.exists(audio_path):
            return audio_path

    except Exception as e:
        print("AUDIO EXTRACTION ERROR:", e)

    return None


# Speech to Text

def speech_to_text(audio_path: str):

    if not audio_path:
        return ""

    if not os.path.exists(audio_path):
        return ""

    try:

        result = model.transcribe(
            audio_path,
            fp16=False
        )

        text = result.get("text", "")

        if text:
            return text.strip()

    except Exception as e:
        print("WHISPER ERROR:", e)

    return ""