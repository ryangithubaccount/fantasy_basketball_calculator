import os
from analysis_files.placement_to_string import placement_to_string

def return_default():
    script_dir = os.path.dirname(__file__)
    rel_path = "../text_files/default_predictions.txt"
    abs_path = os.path.join(script_dir, rel_path)
    f = open(abs_path, 'r')
    text = f.readlines()
    predictions = []
    last_year_rankings = []
    for line in text:
        #name, predicted rank, last year rank, difference
        line = line.split(',')
        predictions.append(line)
    last_year_rankings = sorted(predictions, key = lambda x:int(x[2]))
    movement = sorted(predictions[:120], key=lambda x:int(x[3]))
    top_gainers = movement[-1:-6:-1]
    top_losers = movement[:5]
    placement_to_string(120, predictions)
    placement_to_string(5, top_gainers)
    placement_to_string(5, top_losers)
    return predictions, last_year_rankings, top_gainers, top_losers