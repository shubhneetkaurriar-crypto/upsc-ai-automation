import re


def normalize(text):
    text = text.lower()
    text = re.sub(r'[^a-z0-9 ]', '', text)
    text = " ".join(text.split())
    return text


def is_duplicate(title, existing_titles):

    current = normalize(title)

    for old_title in existing_titles:

        if normalize(old_title) == current:
            return True

    return False
