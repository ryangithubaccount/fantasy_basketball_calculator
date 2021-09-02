import os
import pandas as pd
import numpy
import matplotlib.pyplot as plt

def extrapolate(nums, year, averages):
    #RETURNS: expected percent change for next year
    #we know by what percentage the performance changes each year
    #sometimes it improves, sometimes it drops
    last_known = 0
    loc = 0
    for i in range(year):
        if not numpy.isnan(nums[i]):
            last_known = nums[i]
            loc = i
    if year > 4:
        projected = last_known + (-0.0235) * (year - loc) 
    else:
        projected = last_known + (-0.17333) * (year - loc)
    if projected > averages[year] * 2 and projected > 0:
        projected = averages[year] * 2
    elif projected < averages[year] * 2 and projected < 0:
        projected = averages[year] * 2
    return projected

#OPENING FILES
script_dir = os.path.dirname(__file__)
rel_path_score_change = 'csv_files/player_score_changes.csv'
abs_file_path_score_change = os.path.join(script_dir, rel_path_score_change)

rel_path_score = 'csv_files/player_scores.csv'
abs_file_path_score = os.path.join(script_dir, rel_path_score)
player_scores = pd.read_csv(abs_file_path_score)

player_score_change = pd.read_csv(abs_file_path_score_change)
averages = player_score_change.mean(axis='columns')
correlations = player_score_change.corr()
columns = player_score_change.columns

rel_path2 = 'text_files/active_players.txt'
abs_file_path2 = os.path.join(script_dir, rel_path2)

f = open(abs_file_path2, 'r')
active_players = f.readlines()
f.close()


#SET VARIABLES
player_num = len(columns)
predictions = []


#MAKING DICTIONARIES
player_indices_dict = {}
for i in range(player_num):
    player_indices_dict[columns[i]] = i

year_scores_dict = {}
sorted_year_indices = {}
for i in range(24):
    temp = []
    for j in range(player_num):
        temp.append(player_scores.loc[i][columns[j]])
    year_scores_dict[i] = temp
    sorted_year_indices[i] = numpy.argsort(temp)


#CALCULATING NEXT YEAR'S OUTPUT
for player in active_players:
    #Calculated from: 30% average, 30% extrapolation, 40% average +/- or 40% correlation
    player = player[:-1]
    personal_stats = numpy.array(player_score_change[player])
    year = 0
    for i in range(24):
        if not numpy.isnan(personal_stats[i]):
            year = i
    year += 1
    chosen_influence = 0
    last_year_score = player_scores[player][year - 1]
    flag = 'corr'
    #less than 5 years of experience
    if numpy.count_nonzero(numpy.isnan(personal_stats)) >= 20:
        #calculate by averages
        #chosen_influence is good/medium/bad average
        #different for year = 1

        sorted_scores = sorted_year_indices[year - 1]
        #find the indice of the player
        player_index = player_indices_dict[player]
        breakpoint = 0
        for i in range(player_num):
            if sorted_scores[i] == player_index:
                breakpoint = i
                break

        close_scores_next_year = []
        for i in range(breakpoint - 10, breakpoint + 20):
            if i > -1 and i < player_num:
                #the next year's score for the next people
                temp_score = year_scores_dict[year][sorted_scores[i]]
                #this is locating the incorrect score (idx is not correct atm)
                if not numpy.isnan(temp_score):
                    close_scores_next_year.append(temp_score)

        chosen_influence = numpy.mean(close_scores_next_year)
        flag = 'mean'
        #print(player)
        #print(chosen_influence)
        

    #greater than or equal to 5 years of experience
    else:
        #calculate by correlation
        #the way to find the n largest element indices in an array:
        #array = numpy.array([i, j, k])
        #indices = numpy.argpartition(array, -n)[:-n] (sorts around the nth largest element and then selects the largest n)
        #we have >2100 people, let's use the top 500 correlations
        personal_corr = numpy.array(correlations[player])
        indices = numpy.argpartition(personal_corr, -100)[-100:]
        year_scores = []
        for index in indices:
            score = player_score_change[columns[index]][year]
            if not numpy.isnan(score):
                year_scores.append(score)
        if not year_scores:
            chosen_influence = last_year_score * (1 + averages[year])
        else:
            chosen_influence = numpy.mean(year_scores)
            chosen_influence = last_year_score * (1 + chosen_influence)
        #print(player)
        #print(chosen_influence)

    #Extrapolation and average part
    extrapo = extrapolate(personal_stats, year, averages)
    avg = averages[year]
    extrapo = last_year_score * (1 + extrapo) * 0.3
    #print(player)
    #print(extrapo)
    avg = last_year_score * (1 + avg) * 0.6
    chosen_influence *= 0.4
    next_year_score = chosen_influence
    predictions.append((player, next_year_score, flag, last_year_score))

predictions = sorted(predictions, key=lambda x:x[1])
for prediction in predictions:
    print(prediction)