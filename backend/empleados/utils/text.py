# utils/text.py

def normalize_name(value):
    return value.strip().title()

def normalize_email(value):
    return value.strip().lower()

def normalize_text(value):
    return value.strip()