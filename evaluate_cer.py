import json
from evaluate import load
from itertools import product
cer = load("cer")

# Read JSON data from file
with open("common-voice-15-transcriptions.json", "r", encoding="utf-8") as f:
    transcript_json = json.load(f)

references = []
best_predictions = []
closest_predictions = []

# Iterate over each sentence in the transcript
for entry in transcript_json:
    reference = entry["sentence"]
    references.append(reference)

    """
    Best prediction outputted by the ASR
    """
    best_segments = [segment["substring"] for segment in entry["segments"]]
    prediction = "".join(best_segments)
    best_predictions.append(prediction)

    # Prepare a list of lists, where each inner list contains the substring
    # and its alternativeSubstrings.
    all_segment_options = []
    for segment in entry["segments"]:
        options = [segment["substring"]] + segment.get("alternativeSubstrings", [])
        all_segment_options.append(options)
    
    """
    Find the closest prediction to the reference among all alternative segments
    """
    # Generate all possible combinations of segments and alternative segments.
    all_combinations = product(*all_segment_options)

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
