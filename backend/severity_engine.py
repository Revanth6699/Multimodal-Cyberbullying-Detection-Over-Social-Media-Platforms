import re

# Obfuscated word normalization

def normalize_obfuscated_text(text):

    replacements = {
        "1": "i",
        "3": "e",
        "4": "a",
        "5": "s",
        "7": "t",
        "0": "o",
        "@": "a",
        "$": "s",
        "!": "i"
    }

    normalized = ""

    for char in text.lower():
        normalized += replacements.get(char, char)

    return normalized


# Safe Word matching

def extract_matched_words(text, word_dict, category):

    text = normalize_obfuscated_text(text)

    words = re.findall(r"\b[a-zA-Z]+\b", text)

    matches = []

    for w in words:
        if w in word_dict:
            matches.append({
                "word": w,
                "category": category
            })

    return matches


# Severity Calculation

def calculate_severity_and_confidence(matches):

    if not matches:
        return 0, 0, None

    severity_score = 0
    trigger_word = None

    for m in matches:

        # Defensive coding (accept string or dict)
        if isinstance(m, str):
            word = m
            category = "offensive"
        else:
            word = m.get("word")
            category = m.get("category")

        if trigger_word is None:
            trigger_word = word

        if category == "explicit":
            severity_score += 3
        elif category == "offensive":
            severity_score += 2
        else:
            severity_score += 1

    severity = min(5, severity_score)

    confidence = min(1.0, severity_score / 5)

    return severity, round(confidence, 2), trigger_word