# Phoneme Decoder Tool for Custom Major System (Jupyter Notebook Form)

import os
import re
from collections import defaultdict
import urllib.request

# Define phoneme-to-digit map based on user-modified major mnemonic system
arpabet_to_digit = {
    'S': '0', # soft
    'Z': '0', # soft
    'T': '1',
    'D': '1',
    'TH': '1',
    'N': '2',
    'M': '3',
    'R': '4',
    'L': '5',
    'CH': '6', # soft
    'JH': '6', # soft
    'SH': '6', # soft
    'ZH': '6', # soft
    'F': '8', 'V': '8',
    'P': '9', 'B': '9',
    'K': '7', 'G': '7',  # hard consonants
    'NG': '7', 'Q': '7', 'C': '7'  # C is ambiguous, treated as hard here
}

"""
0   s,z,soft c
1   t, d, th
2   n
3   m
4   r
5   l
6   ch, j, soft g, sh
7   K, hard c, q, hard g, ng
8   f, v, ph
9   p, b

Unassigned   h, y, w, vowels, silent letters

"""


# Vowel sounds in ARPAbet (ignored)
vowel_phones = {"AA", "AE", "AH", "AO", "AW", "AY", "EH", "ER", "EY",
                 "IH", "IY", "OW", "OY", "UH", "UW"}

# Download CMU Pronouncing Dictionary
def download_cmudict():
    url = "https://svn.code.sf.net/p/cmusphinx/code/trunk/cmudict/cmudict.0.7a"
    local_file = "cmudict.0.7a"
    if not os.path.exists(local_file):
        urllib.request.urlretrieve(url, local_file)
    return local_file

# Parse CMUdict and return digit-to-word map based on phoneme encoding
def parse_cmudict(filepath):
    digit_map = defaultdict(list)
    with open(filepath, "r") as f:
        for line in f:
            if line.startswith(";"):  # comment line
                continue
            parts = line.strip().split("  ")
            if len(parts) != 2:
                continue
            word, pronunciation = parts
            phonemes = pronunciation.split()
            digits = ""
            for phone in phonemes:
                base = re.sub(r"\d", "", phone)  # remove stress markers
                if base in vowel_phones:
                    continue
                if base in arpabet_to_digit:
                    digits += arpabet_to_digit[base]
            if digits:
                digit_map[digits].append(word.lower())
    return digit_map

# Match encoded string to possible words from digit map
def match_encoded_sequence(encoded, digit_map, min_len=3, max_len=10):
    matches = []
    for start in range(len(encoded)):
        for end in range(start + min_len, min(start + max_len, len(encoded)) + 1):
            chunk = encoded[start:end]
            if chunk in digit_map:
                for word in digit_map[chunk]:
                    matches.append((start, end, chunk, word))
    return matches

# Example usage
# 1. Download dict
# 2. Build map
# 3. Run match on digit string
encoded_input = "2210740184"  # your full digit stream here
digit_map = parse_cmudict(download_cmudict())
matches = match_encoded_sequence(encoded_input, digit_map)
for match in matches:
    print(match)  # (start, end, digits, word)




print("Notebook-ready script initialized. Fill in your encoded input and run the match logic to see results.")