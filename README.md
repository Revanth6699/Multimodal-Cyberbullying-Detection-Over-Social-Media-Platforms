# Multimodal Cyberbullying Detection Over Social Media Platforms
A real-time moderation system that detects cyberbullying from text, audio, video, datasets, and social media URLs using NLP and speech recognition.

## Problem Statement
Cyberbullying has become a major issue across social media platforms. Most existing systems focus only on text-based moderation and fail to process multimedia content such as audio and video. This project addresses that gap by extracting text from audio/video content and analyzing it using NLP-based cyberbullying detection techniques.

## Features
1. Text toxicity detection
2. Audio-to-text moderation
3. Video-to-audio extraction and moderation
4. URL moderation (YouTube, Instagram, Facebook, WhatsApp links)
5. Offensive and explicit word detection
6. Severity scoring (0–5)
   - Confidence score generation
7. Dataset evaluation
   - Accuracy
   - F1 - Score
   - Recall
   - Percision
   - Confusion matrix visualization
8. Streamlit moderation dashboard

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
1. FFmpeg
2. yt-dlp
### Algorithms
1. Regex Tokenization
2. Dictionary Matching
3. Fuzzy Matching
4. Severity Scoring
5. Confusion Matrix Evaluation

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
1. Accuracy
2. Precision
3. Recall
4. F1 Score
5. Confusion Matrix

## Tech Stack
1. Python
2. FastAPI
3. Streamlit
4. Transformers
5. Whisper
6. FFmpeg
7. yt-dlp
8. Scikit-learn
9. Matplotlib

## Installation
```bash
git clone https://github.com/Revanth6699/Multimodal-Cyberbullying-Detection-Over-Social-Media-Platforms.git
cd multimodal-cyberbullying-detection
pip install -r requirements.txt
```
```
## Run Backend
uvicorn backend.main:app --reload
```

```
## Run Frontend
streamlit run frontend/app.py
```

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
1. OCR integration for image moderation
2. Facial expression detection
3. Gesture analysis
4. Real-time streaming moderation
5. Database integration
