# Multimodal Cyberbullying Detection Over Social Media Platforms
A real-time moderation system that detects cyberbullying from text, audio, video, datasets, and social media URLs using NLP and speech recognition.

## Problem Statement
Cyberbullying has become a major issue across social media platforms. Most existing systems focus only on text-based moderation and fail to process multimedia content such as audio and video. This project addresses that gap by extracting text from audio/video content and analyzing it using NLP-based cyberbullying detection techniques.

## Features
-> Text toxicity detection
-> Audio-to-text moderation
-> Video-to-audio extraction and moderation
-> URL moderation (YouTube, Instagram, Facebook, WhatsApp links)
-> Offensive and explicit word detection
-> Severity scoring (0–5)
=> Confidence score generation
-> Dataset evaluation
=> Accuracy
=> F1 - Score
=> Recall
=> Percision
=> Confusion matrix visualization
-> Streamlit moderation dashboard

## Supported Inputs
Input Type | Processing |
-----------|------------|
Text | Direct NLP analysis 
Audio | Speech-to-text using Whisper 
Video | Audio extraction using FFmpeg + Whisper
URL | Media extraction using yt-dlp
Dataset | Evaluation metrics generation

## Models and Algorithms Used
### NLP Model
-> Toxic-BERT (Transformer-based model)
### Speech Recognition
-> OpenAI Whisper
### Media Processing
-> FFmpeg
-> yt-dlp
### Algorithms
-> Regex Tokenization
-> Dictionary Matching
-> Fuzzy Matching
-> Severity Scoring
-> Confusion Matrix Evaluation

## Pipeline
Input → Text Extraction → NLP Analysis → Severity Engine → Moderation Result

## Severity Calculation
Severity is calculated using weighted scoring:

```python
severity = min(5, (2 * offensive_words + 3 * explicit_words))
```

### Severity Levels
Severity | Meaning |
--------|----------|
0 | No abuse |
1-2 | Low |
3-4 | Moderate |
5 | High |

## Evaluation Metrics
-> Accuracy
-> Precision
-> Recall
-> F1 Score
-> Confusion Matrix

## Tech Stack
-> Python
-> FastAPI
-> Streamlit
-> Transformers
-> Whisper
-> FFmpeg
-> yt-dlp
-> Scikit-learn
-> Matplotlib

## Installation
git clone https://github.com/Revanth6699/Multimodal-Cyberbullying-Detection-Over-Social-Media-Platforms.git
cd multimodal-cyberbullying-detection
pip install -r requirements.txt

## Run Backend
uvicorn backend.main:app --reload

## Run Frontend
streamlit run frontend/app.py

## Screenshots
<img width="1920" height="1080" alt="dataset 2" src="https://github.com/user-attachments/assets/2226a4fb-64cf-46e7-9901-120d75a2fe21" />
<img width="1920" height="1080" alt="url2" src="https://github.com/user-attachments/assets/bfa310e8-b6dd-4f3c-88fd-272eb1706da4" />
<img width="1920" height="1080" alt="video 2" src="https://github.com/user-attachments/assets/91557219-ffb9-4528-8657-568c08c50bf6" />
<img width="1920" height="1080" alt="text 2" src="https://github.com/user-attachments/assets/5ec9a4fa-8b5a-4428-9101-2cb2f40b1d7a" />

### Dataset Evaluation
<img width="600" height="500" alt="confusion_matrix_60aa4a1d2c404022bf25fb71ec754c05" src="https://github.com/user-attachments/assets/cedf0f81-4284-4998-970b-1ea0fee54a19" />


## Limitations
1. Primarily optimized for English
2. No OCR-based image moderation
3. No gesture or facial expression detection
4. Depends on speech clarity in audio/video

## Future Improvements
-> OCR integration for image moderation
-> Facial expression detection
-> Gesture analysis
-> Real-time streaming moderation
-> Database integration
