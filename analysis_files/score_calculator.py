import pandas as pd
import os

def calculate_overall_scores(point_system):
    def calculate_score(data, point_system):
        #ESPN Fantasy's new default scoring system is as follows:
        #PT (1); 3PM (1); FGA (-1); FGM (2); FTA (-1); FTM (1); REB (1); AST (2); STL (4); BLK (4); TOV (-2)
        #indices are 24, 6, 4, 3, 13, 14, 18, 19, 20, 21, 22 (add one since the year is at the front)

        #should be '20xx:'
        year = data[0][0:4]

        #using the point values above
        score = 0
        score += float(data[25]) * point_system[0] + float(data[7]) * point_system[1] + float(data[5]) * point_system[2]\
         + float(data[4]) * point_system[3] + float(data[15]) * point_system[4] + float(data[14]) * point_system[5]\
          + float(data[19]) * point_system[6] + float(data[20]) * point_system[7] + float(data[21]) * point_system[8]\
           + float(data[22]) * point_system[9] + float(data[23]) * point_system[10]

        score = float('%.2f' % score)
        score_tot = score * int(data[1])
        score_pg = score

        #adjust due to differences in games from COVID
        if year == '2020':
            score_tot = float('%.2f' % (score_tot * 82.0 / 70.0))
        elif year == '2021':
            score_tot = float('%.2f' % (score_tot * 82.0 / 72.0))
        return 0.8 * 82 * score_pg + 0.2 * score_tot
        #end function

    script_dir = os.path.dirname(__file__)

    rel_path1 = '../text_files/player_stats.txt'
    abs_file_path1 = os.path.join(script_dir, rel_path1)
    f = open(abs_file_path1, 'r')

    text = f.readlines()
    names = []
    scores = []
    score_changes = []
    years = []
    #number of players in the dataset
    n = len(text)
    #we want a 24 x n matrix
    for i in range(24):
        scores.append([])
        score_changes.append([])
        years.append(i)
    i = 0
    while i < n:
        year_count = 1
        line = text[i].split()
        if len(line) < 10:
            names.append(text[i][0:len(text[i]) - 1])
            i += 1
            first_year = int(text[i])
            i += 1
            line = text[i].split()
            while len(line) > 10:
                year = int(line[0][0:4]) - first_year
                while year > year_count:
                    scores[year_count - 1].append(float("NaN"))
                    year_count += 1

                scores[year - 1].append(calculate_score(line, point_system))
                i += 1
                year_count += 1
                #avoid going out of bounds
                if i == n:
                    break
                line = text[i].split()
            while year_count < 25:
                scores[year_count - 1].append(float("NaN"))
                year_count += 1
            #calculate score changes
            for j in range(24):
                if j == 0:
                    score_changes[j].append(float("NaN"))
                    continue
                prev = scores[j - 1][-1]
                curr = scores[j][-1]
                if prev and curr:
                    score_changes[j].append((curr - prev) / prev)
                else:
                    score_changes[j].append(float("NaN"))
        i += 1

    player_scores = pd.DataFrame(scores, index=years, columns=names)
    player_score_change = pd.DataFrame(score_changes, index=years, columns=names)
    dictionary = {}
    dictionary['player_scores'] = player_scores
    dictionary['player_score_changes'] = player_score_change
    return dictionary