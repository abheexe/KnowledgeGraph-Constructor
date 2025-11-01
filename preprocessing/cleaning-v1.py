import json
import re

def clean_line_breaks(text):
    # Replace newlines in the middle of words or sentences with space
    text = re.sub(r'(?<!\n)\n(?!\n)', ' ', text)
    # Collapse multiple whitespaces into one space
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def is_table_artifact(sentence):
    # Heuristic to identify probable table rows or numeric-only fragments
    num_chars = sum(c.isdigit() for c in sentence)
    alpha_chars = sum(c.isalpha() for c in sentence)
    # If more than half are digits or sentence is very short => likely table or noise
    if num_chars > alpha_chars or len(sentence) < 20:
        return True
    # Filter out sentences with excessive special characters common in tables
    if re.search(r'[\[\]\(\),:;%\$]', sentence) and num_chars > 5:
        return True
    return False

def is_valid_sentence(sentence):
    # Check min word count and length to discard junk lines
    return len(sentence.split()) > 5 and len(sentence) > 30

def clean_sentences(sentences):
    cleaned = []
    for s in sentences:
        s = clean_line_breaks(s)
        if is_valid_sentence(s) and not is_table_artifact(s):
            cleaned.append(s)
    return cleaned

# Load your existing JSON of extracted sentences
with open('extracted_sentences.json', 'r', encoding='utf-8') as f:
    all_sentences = json.load(f)

all_cleaned = {}

for file_path, sentences in all_sentences.items():
    cleaned = clean_sentences(sentences)
    all_cleaned[file_path] = cleaned
    print(f"Cleaned {len(cleaned)} sentences from {file_path}")

# Save cleaned sentences to a new JSON file
with open('cleaned_sentences.json', 'w', encoding='utf-8') as f:
    json.dump(all_cleaned, f, ensure_ascii=False, indent=4)

print("Saved cleaned sentences to cleaned_sentences.json")

