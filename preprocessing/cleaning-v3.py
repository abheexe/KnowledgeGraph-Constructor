import json
import re
import string
import wordninja 

def clean_line_breaks(text):
    text = re.sub(r'(?<!\n)\n(?!\n)', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def is_table_artifact(sentence):
    num_chars = sum(c.isdigit() for c in sentence)
    alpha_chars = sum(c.isalpha() for c in sentence)
    repeated_punct = re.search(r'([\.\,\-\/])\1{3,}', sentence)

    if num_chars > alpha_chars:
        return True
    if repeated_punct:
        return True
    if len(re.findall(r'[^\w\s]', sentence)) > 15:
        return True
    if len(sentence) < 20:
        return True
    return False

def fix_concatenated_words(sentence):
    if ' ' not in sentence:
        return ' '.join(wordninja.split(sentence))
    return sentence

def is_formula_or_noise(sentence):
    math_symbols = set('=+-/*^\n()<>{}[]σπλτ∞∑∫∂≥≤≠√')
    if len(sentence) == 0:
        return True
    alpha_count = sum(c.isalpha() for c in sentence)
    symbol_count = sum(1 for c in sentence if c in math_symbols)
    if symbol_count > alpha_count or alpha_count < 10:
        return True
    return False

def is_garbage(sentence):
    alpha_chars = sum(1 for c in sentence if c.isalpha())
    total_len = len(sentence)
    if total_len == 0 or alpha_chars / total_len < 0.4:
        return True
    if any(sentence.count(c) > total_len * 0.3 for c in set(sentence)):
        return True
    return False

def is_valid_sentence(sentence):
    return len(sentence.split()) > 5 and len(sentence) > 30

def clean_sentences(sentences):
    cleaned = []
    for s in sentences:
        s = clean_line_breaks(s)
        s = fix_concatenated_words(s)
        if (
            is_valid_sentence(s) 
            and not is_table_artifact(s) 
            and not is_formula_or_noise(s) 
            and not is_garbage(s)
        ):
            cleaned.append(s)
    return cleaned

# Load your further cleaned JSON
with open('cleaned_sentences2.json', 'r', encoding='utf-8') as f:
    all_sentences = json.load(f)

all_final_cleaned = {}

for file_path, sentences in all_sentences.items():
    cleaned = clean_sentences(sentences)
    all_final_cleaned[file_path] = cleaned
    print(f"Final cleaned {len(cleaned)} sentences from {file_path}")

with open('final_cleaned_sentences.json', 'w', encoding='utf-8') as f:
    json.dump(all_final_cleaned, f, ensure_ascii=False, indent=4)

print("Saved final cleaned sentences to final_cleaned_sentences.json")
