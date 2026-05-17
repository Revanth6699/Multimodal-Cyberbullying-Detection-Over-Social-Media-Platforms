import os
import json

DATA_DIR = "data"

OFFENSIVE_FILE = os.path.join(DATA_DIR, "offensive_words.json")
EXPLICIT_FILE = os.path.join(DATA_DIR, "explicit_words.json")


# Load word to dictionarie

def load_word_dicts():

    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)

    if not os.path.exists(OFFENSIVE_FILE):
        with open(OFFENSIVE_FILE, "w") as f:
            json.dump({}, f)

    if not os.path.exists(EXPLICIT_FILE):
        with open(EXPLICIT_FILE, "w") as f:
            json.dump({}, f)

    with open(OFFENSIVE_FILE) as f:
        offensive = json.load(f)

    with open(EXPLICIT_FILE) as f:
        explicit = json.load(f)

    return offensive, explicit


# Save word to dictionary

def save_dict(path, data):

    with open(path, "w") as f:
        json.dump(data, f, indent=2)


# ADD Word

def add_word(word, category, severity=2):

    word = word.lower().strip()

    offensive, explicit = load_word_dicts()

    if category == "offensive":

        offensive[word] = severity
        save_dict(OFFENSIVE_FILE, offensive)

        return {"message": f"{word} added to offensive words"}

    elif category == "explicit":

        explicit[word] = severity
        save_dict(EXPLICIT_FILE, explicit)

        return {"message": f"{word} added to explicit words"}

    else:

        return {"error": "category must be offensive or explicit"}


# Auto ADD Predicted word

def add_predicted_word(word, base_word, severity=2):

    word = word.lower().strip()

    offensive, explicit = load_word_dicts()

    # determine category from base word
    if base_word in explicit:

        explicit[word] = severity
        save_dict(EXPLICIT_FILE, explicit)

        return {"message": f"{word} added to explicit_words"}

    else:

        offensive[word] = severity
        save_dict(OFFENSIVE_FILE, offensive)

        return {"message": f"{word} added to offensive_words"}


# DELETE Word

def delete_word(word):

    word = word.lower().strip()

    removed = False

    offensive_words, explicit_words = load_word_dicts()

    if word in offensive_words:
        del offensive_words[word]
        removed = True

    if word in explicit_words:
        del explicit_words[word]
        removed = True

    # save back correctly as JSON
    save_dict(OFFENSIVE_FILE, offensive_words)
    save_dict(EXPLICIT_FILE, explicit_words)

    if removed:
        return {"message": f"{word} removed successfully"}

    return {"message": f"{word} not found"}