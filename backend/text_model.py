from transformers import pipeline
import warnings

warnings.filterwarnings("ignore")

classifier = pipeline(
    "text-classification",
    model="unitary/toxic-bert",
    truncation=True,
    device=-1   # force CPU, avoid CUDA warnings
)

def detect_bullying(text: str):

    if not text:
        return "neutral", 0.0

    result = classifier(text[:512])[0]

    label = result["label"].lower()
    score = float(result["score"])

    return label, score