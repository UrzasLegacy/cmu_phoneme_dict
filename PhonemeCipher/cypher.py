import re
from itertools import product
from difflib import get_close_matches

# Define the custom major mnemonic system as phoneme options per digit
phoneme_map = {
    '0': ['s', 'z', 'c'],  # soft c
    '1': ['t', 'd', 'th'],
    '2': ['n'],
    '3': ['m'],
    '4': ['r'],
    '5': ['l'],
    '6': ['ch', 'j', 'g', 'sh'],  # soft g
    '7': ['k', 'c', 'q', 'g', 'ng'],  # hard g
    '8': ['f', 'v', 'ph'],
    '9': ['p', 'b']
}

# The full encoded string
encoded_string = (
    "22107401846221320055299317010112114951882139150740215792305821740381673572344629"
    "86415735318421090011047103204121113200791130126721211501121011030585301109079512"
    "72121123011571154719478140784305241070301820718410158433941065194701112074216263"
    "0111770"
)

# Step 1: Convert digits to possible phoneme sets
phoneme_options = [phoneme_map[d] for d in encoded_string]

# Step 2: Build a stream of the first possible phoneme choice (simplified single-path decode)
primary_phoneme_stream = [opts[0] for opts in phoneme_options]
phoneme_string = ''.join(primary_phoneme_stream)

# Step 3: Try to segment into likely English words using a basic dictionary
with open("/usr/share/dict/words") as f:
    english_words = set(word.strip().lower() for word in f if word[0].islower())

# Helper to segment phoneme string into plausible words
def segment_words(phonemes, dictionary):
    words = []
    i = 0
    while i < len(phonemes):
        for j in range(len(phonemes), i, -1):
            chunk = phonemes[i:j]
            candidates = get_close_matches(chunk, dictionary, n=1, cutoff=0.8)
            if candidates:
                words.append(candidates[0])
                i = j
                break
        else:
            # If no match found, move forward one character
            words.append(phonemes[i])
            i += 1
    return words

# Segment the phoneme stream
segmented_words = segment_words(phoneme_string, english_words)

# Display the segmented output
import ace_tools as tools; tools.display_dataframe_to_user(name="Decoded Phoneme Segments", dataframe={'Word': segmented_words})
