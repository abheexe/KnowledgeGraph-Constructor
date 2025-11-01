import os
import pdfplumber
import spacy

import json

nlp = spacy.load("en_core_web_sm")
root_folder = 'papers'

all_sentences = {}

def extract_text_from_pdf(pdf_path):
    text = ""
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
    except Exception as e:
        print(f"Error reading {pdf_path}: {e}")
    return text

def process_text(text):
    doc = nlp(text)
    sentences = [sent.text.strip() for sent in doc.sents if sent.text.strip()]
    return sentences

# Recursively process PDFs in all subfolders
for dirpath, dirnames, filenames in os.walk(root_folder):
    for filename in filenames:
        if filename.lower().endswith('.pdf'):
            file_path = os.path.join(dirpath, filename)
            print(f"Processing {file_path} ...")  # Full path for clarity
            raw_text = extract_text_from_pdf(file_path)
            if raw_text.strip():
                sentences = process_text(raw_text)
                all_sentences[file_path] = sentences
                print(f"Extracted {len(sentences)} sentences from {filename}")
            else:
                print(f"No text extracted from {filename}")


with open('extracted_sentences.json', 'w', encoding='utf-8') as f:
    json.dump(all_sentences, f, ensure_ascii=False, indent=4)

print("Saved extracted sentences to extracted_sentences.json")