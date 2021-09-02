import pandas as pd
import os
from collections import defaultdict
import matplotlib.pyplot as plt


def calculate_score(data):
    #ESPN Fantasy's new default scoring system is as follows:
    #Point (1); 3PM (1); FGA (-1); FGM (2); FTA (-1); FTM (1); REB (1); AST (2); STL (4); BLK (4); TOV (-2)
    #indices are 24, 6, 4, 3, 13, 14, 18, 19, 20, 21, 22 (add one since the year is at the front)

    #should be '20xx:'
    year = data[0][0:4]

    #using the point values above
    score = 0
    score += float(data[25]) + float(data[7]) - float(data[5]) + 2 * float(data[4])\
        - float(data[15]) + float(data[14]) + float(data[19]) + 2 * float(data[20])\
            + 4 * float(data[21]) + 4 * float(data[22]) - 2 * float(data[23])

    score = float('%.2f' % score)
    score_tot = score * int(data[1])
    score_pg = score

    #adjust due to differences in games from COVID
    if year == '2020':
        score_tot = float('%.2f' % (score_tot * 82.0 / 70.0))
    elif year == '2021':
        score_tot = float('%.2f' % (score_tot * 82.0 / 72.0))
    return 0.6 * 82 * score_pg + 0.4 * score_tot
    #end function

rel_path = 'text_files/player_stats.txt'
script_dir = os.path.dirname(__file__)
abs_file_path = os.path.join(script_dir, rel_path)
f = open(abs_file_path, 'r')

names = []
text = f.readlines()
player_score_dict = defaultdict(list)
i = 0
n = len(text)
while i < len(text):
    line = text[i].split()
    if len(line) < 10:
        year_scores = [None] * 24
        #player_score_dict['Names'].append(text[i])
        names.append(text[i][:len(text[i]) - 1])
        i += 1
        first_year = int(text[i])
        i += 1
        line = text[i].split()
        while len(line) > 10:
            year = int(line[0][0:4]) - first_year
            year_scores[year - 1] = calculate_score(line)
            i += 1
            #avoid going out of bounds
            if i == n:
                break
            line = text[i].split()
        for x in range(1, 25):
            player_score_dict[str(x)].append(year_scores[x - 1])
    i += 1
player_scores = pd.DataFrame(player_score_dict, index = names)
print(player_scores)
player_scores.plot()
plt.show()