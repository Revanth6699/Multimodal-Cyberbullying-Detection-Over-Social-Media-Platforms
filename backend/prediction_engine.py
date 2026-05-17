from rapidfuzz import fuzz
from backend.word_manager import load_word_dicts

# higher threshold to reduce false positives
SIMILARITY_THRESHOLD = 90


# --------------------------------------------------
# stopwords (never predict these)
# --------------------------------------------------

STOPWORDS = {
    "i","you","he","she","it","we","they",
    "a","an","the","and","or","but",
    "is","are","was","were","be","been","being",
    "have","has","had","do","does","did",
    "to","from","of","in","on","for","with",
    "this","that","these","those",
    "my","your","his","her","their","our",
    "me","him","her","them","us",
    "am","will","shall","can","could",
    "would","should","may","might",
    "very","really","just"
}


# --------------------------------------------------
# leet / obfuscation mapping
# --------------------------------------------------

LEET_MAP = {
    "@": "a",
    "4": "a",
    "3": "e",
    "1": "i",
    "!": "i",
    "0": "o",
    "$": "s",
    "5": "s",
    "7": "t",
    "*": ""
}


# --------------------------------------------------
# detect if token contains obfuscation
# --------------------------------------------------

def has_leet_chars(word: str):

    for c in LEET_MAP.keys():
        if c in word:
            return True

    return False


# --------------------------------------------------
# normalize leet characters
# --------------------------------------------------

def normalize_leet(word: str):

    for char, replacement in LEET_MAP.items():
        word = word.replace(char, replacement)

    return word


# --------------------------------------------------
# clean tokens
# --------------------------------------------------

def clean_token(word: str):

    word = word.lower().strip()

    for char in [".", ",", "!", "?", "'", '"', ":", ";", "(", ")"]:
        word = word.replace(char, "")

    return word


# --------------------------------------------------
# tokenize sentence
# --------------------------------------------------

def tokenize(text: str):

    tokens = []

    for word in text.split():

        token = clean_token(word)

        if len(token) < 3:
            continue

        if token in STOPWORDS:
            continue

        tokens.append(token)

    return tokens


# --------------------------------------------------
# detect abusive variants
# --------------------------------------------------

def predict_unseen_words(text: str):

    offensive_dict, explicit_dict = load_word_dicts()

    dictionary = {**offensive_dict, **explicit_dict}

    tokens = tokenize(text)

    predictions = []

    for token in tokens:

        # skip normal words without obfuscation
        if not has_leet_chars(token):
            continue

        normalized = normalize_leet(token)

        # skip if already known abusive word
        if normalized in dictionary:
            continue

        best_match = None
        best_score = 0
        best_severity = 2

        for dict_word, severity in dictionary.items():

            score = fuzz.ratio(normalized, dict_word)

            if score > best_score:

                best_score = score
                best_match = dict_word
                best_severity = severity

        # require strong similarity
        if best_score >= SIMILARITY_THRESHOLD:

            prediction = {
                "predicted_word": token,
                "base_word": best_match,
                "severity": best_severity,
                "confidence": round(best_score / 100, 2)
            }

            predictions.append(prediction)

    return predictions