import json
from evaluate import load
from itertools import product
import regex as re
import doctest
from tqdm import tqdm

cjk_char_re = re.compile(r'[\p{Unified_Ideograph}\u3006\u3007]')
punctuation_re = re.compile(r'\p{P}')

cer = load("cer")

# Read JSON data from file
with open("guangdong-daily-use-transcriptions.json", "r", encoding="utf-8") as f:
    transcript_json = json.load(f)

references = []
best_predictions = []
closest_predictions = []
sound_closest_predictions = []
sound_closest_references = []

char_sounds = {}
with open("charlist.csv", "r") as charlist:
    for row in map(lambda line: line.strip().split(","), charlist.readlines()):
        char_sounds[row[0]] = row[1:]

def to_sounds(sentence: str, output_tones=True) -> [[str]]:
    """
    Convert a sentence containing Chinese characters, English words,
    punctuations, and potentially other symbols into Jyutping.
    * Keep Chinese characters outside the vocabulary and English words
    as-is.
    * Ignore punctuations, except periods and dashes

    >>> to_sounds('佢行山也')
    [['heoi5', 'keoi5'], ['haang1', 'haang4', 'hang4', 'hang6', 'hong2', 'hong4'], ['saan1'], ['jaa2', 'jaa4', 'jaa5', 'jaa6', 'je1']]
    
    >>> to_sounds('我鍾意Python。')
    [['ngo5'], ['zung1'], ['ji1', 'ji2', 'ji3', 'ji5'], ['Python']]
    
    >>> to_sounds('Hello!')
    [['Hello']]
    
    >>> to_sounds('你好 - Hello!')
    [['nei5'], ['hou2', 'hou3'], ['-'], ['Hello']]

    >>> to_sounds(',,abc,,')
    [['abc']]

    >>> to_sounds('')
    []

    >>> to_sounds('。')
    []

    """
    sounds = []
    segment = ""
    sentence = re.sub(r"\s+", " ", sentence.strip())
    for char in sentence:
        if cjk_char_re.match(char):
            # Flush the previous segment before appending the sounds of the Chinese character
            if len(segment) > 0:
                sounds.append([segment.strip()])
                segment = ""
            if char in char_sounds:
                if output_tones:
                    sounds.append(char_sounds[char])
                else:
                    sounds.append(list(set(map(lambda jyutping: jyutping[:-1], char_sounds[char]))))
            else:
                sounds.append([char])
        elif punctuation_re.match(char) and char != '.' and char != '-':
            # ignore punctuations except periods and dashes
            continue
        elif char == ' ':
            # Flush the previous segment before appending the sounds of the Chinese character
            if len(segment) > 0:
                sounds.append([segment.strip()])
                segment = ""
        else:
            segment += char
    # Flush the previous segment before appending the sounds of the Chinese character
    if len(segment) > 0:
        sounds.append([segment.strip()])
        segment = ""
    return sounds


def normalize_sentence(s: str) -> str:
    return punctuation_re.sub("", s).replace("噶", "㗎").replace("咧", "呢")


def evaluate_cer():
    # Iterate over each sentence in the transcript
    for entry in tqdm(transcript_json):
        reference = normalize_sentence(entry["sentence"])
        references.append(reference)

        """
        Best prediction outputted by the ASR
        """
        best_segments = [segment["substring"] for segment in entry["segments"]]
        best_prediction = "".join(best_segments)
        best_predictions.append(best_prediction)

        """
        Find the closest prediction to the reference among all alternative segments
        """
        # Prepare a list of lists, where each inner list contains the substring
        # and its alternativeSubstrings.
        all_segment_options = []
        for segment in entry["segments"]:
            options = [segment["substring"]] + segment.get("alternativeSubstrings", [])
            all_segment_options.append(options)
        
        # Generate all possible combinations of segments and alternative segments.
        all_combinations = list(product(*all_segment_options))

        min_cer = float('inf')
        closest_prediction = None

        for combination in all_combinations:
            prediction = ''.join(combination)
            
            cer_result = cer.compute(predictions=[prediction], references=[reference])

            if cer_result < min_cer:
                min_cer = cer_result
                closest_prediction = prediction

        closest_predictions.append(closest_prediction)

    cer_score_best = cer.compute(predictions=best_predictions, references=references)
    print(f"CER Score for best predictions: {cer_score_best}")

    cer_score_closest = cer.compute(predictions=closest_predictions, references=references)
    print(f"CER Score for closest predictions: {cer_score_closest}")

if __name__ == "__main__":
    import doctest
    doctest.testmod()
    
    evaluate_cer()
