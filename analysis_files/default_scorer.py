import os

def return_default():
    script_dir = os.path.dirname(__file__)
    rel_path = "../text_files/predictions.txt"
    abs_path = os.path.join(script_dir, rel_path)
    f = open(abs_path, 'r')
    text = f.readlines()
    predictions = []
    last_year_rankings = []
    for line in text:
        #name, predicted rank, last year rank, difference
        line = line.split(',')
        predictions.append(line)
    last_year_rankings = sorted(predictions, key = lambda x:x[2], reverse=True)
    return predictions, last_year_rankings
