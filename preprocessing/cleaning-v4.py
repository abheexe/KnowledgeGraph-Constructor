import json
import re
import wordninja  

def fix_concatenated_words(sentence):
    # If sentence contains spaces, check each token and split if long and merged
    if ' ' in sentence:
        tokens = sentence.split()
        fixed_tokens = []
        for token in tokens:
            # Heuristic: if token >10 chars and only alphanumeric, likely concatenated
            if len(token) > 10 and re.match(r'^[a-zA-Z]+$', token):
                fixed_tokens.append(' '.join(wordninja.split(token)))
            else:
                fixed_tokens.append(token)
        return ' '.join(fixed_tokens)
    else:
        # If no spaces, split entire sentence
        return ' '.join(wordninja.split(sentence))

with open('final_cleaned_sentences.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

fixed_data = {}
for file_path, sentences in data.items():
    fixed_sentences = []
    for sentence in sentences:
        fixed_sentence = fix_concatenated_words(sentence)
        fixed_sentences.append(fixed_sentence)
    fixed_data[file_path] = fixed_sentences
    print(f"Fixed concatenated words in {len(fixed_sentences)} sentences for {file_path}")

with open('fixed_spaces_sentences.json', 'w', encoding='utf-8') as f:
    json.dump(fixed_data, f, ensure_ascii=False, indent=4)

print("Saved fixed sentences with spaces to fixed_spaces_sentences.json")
