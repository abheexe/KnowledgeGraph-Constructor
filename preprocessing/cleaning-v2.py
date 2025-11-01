import json
import re
import wordninja

def clean_line_breaks(text):
    text = re.sub(r'(?<!\n)\n(?!\n)', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def is_table_artifact(sentence):
    # Frequent numeric values or excessive punctuation like repeated dots
    num_chars = sum(c.isdigit() for c in sentence)
    alpha_chars = sum(c.isalpha() for c in sentence)
    # Check for repeated punctuation (e.g., .....)
    repeated_punct = re.search(r'([\.\,\-\/])\1{3,}', sentence)

    if num_chars > alpha_chars:
        return True
    if repeated_punct:
        return True
    # Filter sentences with too many non-alphanumerics or weird chars
    if len(re.findall(r'[^\w\s]', sentence)) > 15:
        return True
    # Also filter short sentences here
    if len(sentence) < 20:
        return True

    return False

def fix_concatenated_words(sentence):
    # Use wordninja to split joined words where no spaces present
    # Only apply if no spaces in sentence
    if ' ' not in sentence:
        return ' '.join(wordninja.split(sentence))
    else:
        return sentence

def is_formula_or_noise(sentence):
    # Detect lines dominated by math-like symbols or very few alphabetics
    math_symbols = set('=+-/*^\\n()<>{}[]σπλτ∞∑∫∂≥≤≠√')
    if len(sentence) == 0:
        return True

    alpha_count = sum(c.isalpha() for c in sentence)
    symbol_count = sum(1 for c in sentence if c in math_symbols)

    # Heuristic: if symbols dominate or alpha very low, treat as noise/formula
    if symbol_count > alpha_count or alpha_count < 10:
        return True

    return False

def is_valid_sentence(sentence):
    # Must have at least 5 words and length >30
    return len(sentence.split()) > 5 and len(sentence) > 30

def clean_sentences(sentences):
    cleaned = []
    for s in sentences:
        s = clean_line_breaks(s)
        s = fix_concatenated_words(s)
        if is_valid_sentence(s) and not is_table_artifact(s) and not is_formula_or_noise(s):
            cleaned.append(s)
    return cleaned

# Load your cleaned JSON
with open('cleaned_sentences.json', 'r', encoding='utf-8') as f:
    all_sentences = json.load(f)

all_further_cleaned = {}

for file_path, sentences in all_sentences.items():
    cleaned = clean_sentences(sentences)
    all_further_cleaned[file_path] = cleaned
    print(f"Further cleaned {len(cleaned)} sentences from {file_path}")

with open('cleaned_sentences2.json', 'w', encoding='utf-8') as f:
    json.dump(all_further_cleaned, f, ensure_ascii=False, indent=4)

print("Saved further cleaned sentences to cleaned_sentences2.json")
