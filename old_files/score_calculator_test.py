import pandas
from collections import defaultdict
import os

script_dir = os.path.dirname(__file__)
rel_path = 'text_files/harden_stats.txt'
abs_file_path = os.path.join(script_dir, rel_path)
f = open(abs_file_path, 'r')

text = f.readlines()
#ESPN Fantasy's new default scoring system is as follows:
#Point (1); 3PM (1); FGA (-1); FGM (2); FTA (-1); FTM (1); REB (1); AST (2); STL (4); BLK (4); TOV (-2)
#indices are 24, 6, 4, 3, 13, 14, 18, 19, 20, 21, 22 (add one since the year is at the front)
score_pg = defaultdict(list)
score_tot = defaultdict(list)

for line in text:
    line_split = line.split(' ')
    if len(line_split) < 27:
        continue

    #should be '20xx:'
    year = line_split[0][0:4]

    #using the point values above
    score = 0
    score += float(line_split[25]) + float(line_split[7]) - float(line_split[5]) + 2 * float(line_split[4])\
         - float(line_split[15]) + float(line_split[14]) + float(line_split[19]) + 2 * float(line_split[20])\
             + 4 * float(line_split[21]) + 4 * float(line_split[22]) - 2 * float(line_split[23])

    score = float('%.2f' % score)
    score_tot[year] = score * int(line_split[1])
    score_pg[year] = score

#adjust due to differences in games from COVID
score_tot['2020'] = float('%.2f' % (score_tot.get('2020') * 82.0 / 70.0))
score_tot['2021'] = float('%.2f' % (score_tot.get('2021') * 82.0 / 72.0))
f.close()

#write into text document
rel_path = 'text_files/harden_score.txt'
abs_file_path = os.path.join(script_dir, rel_path)
f = open(abs_file_path, 'w')
#name
f.write(text[0])
f.write('year: pg   total\n')
for year in score_tot.keys():
    f.write(year + ': ' + str(score_pg[year]) + ' ' + str(score_tot[year]) + '\n')
f.close()