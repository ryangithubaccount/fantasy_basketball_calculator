import os
import numpy
from collections import defaultdict

def predict_pattern(player_scores, player_score_change):
    script_dir = os.path.dirname(__file__)
    #rel_path = "../csv_files/player_score_changes.csv"
    #abs_path = os.path.join(script_dir, rel_path)
    #player_score_change = pd.read_csv(abs_path)
    averages = player_score_change.mean(axis='columns')
    correlations = player_score_change.corr()
    columns = player_score_change.columns

    rel_path2 = '../text_files/active_players.txt'
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
            #previously at columns[j] (the name)
            temp.append(player_scores.loc[i][j])
        year_scores_dict[i] = temp
        sorted_year_indices[i] = numpy.argsort(temp)


    #CALCULATING NEXT YEAR'S OUTPUT
    for index in range(len(active_players)):
        player = active_players[index][:-1]
        #Calculated from: 30% average, 30% extrapolation, 40% average +/- or 40% correlation
        personal_stats = numpy.array(player_score_change.iloc[:,player_indices_dict[player]])
        personal_scores = numpy.array(player_scores.iloc[:,player_indices_dict[player]])
        year = 0
        for i in range(24):
            if not numpy.isnan(personal_scores[i]):
                year = i
        year += 1
        chosen_influence = 0
        last_year_score = personal_scores[year - 1]
        if not numpy.isnan(personal_stats[year - 2]) and (personal_stats[year - 1] < -0.125 or (personal_stats[year - 1] > 0.1 and personal_stats[year - 1] < 0.2)):
            #weights the last two years if there is a significant drop in performance
            last_year_score = personal_scores[year - 1] * 0.6 + personal_scores[year - 2] * 0.4
        flag = 'corr'
        #calculate by correlation
        #the way to find the n largest element indices in an array:
        #array = numpy.array([i, j, k])
        #indices = numpy.argpartition(array, -n)[:-n] (sorts around the nth largest element and then selects the largest n)
        #we have >2100 people, let's use the top 100 correlations
        personal_corr = numpy.array(correlations[player])
        try:
            indices = numpy.argpartition(personal_corr, -100)[-100:]
        except ValueError:
            continue
        year_scores = []
        for index in indices:
            score = player_score_change.loc[year][index]
            if not numpy.isnan(score):
                year_scores.append(score)
        if not year_scores:
            corr = last_year_score * (1 + averages[year])
        else:
            corr = numpy.mean(year_scores)
            corr = last_year_score * (1 + chosen_influence)


        if numpy.count_nonzero(numpy.isnan(personal_stats)) >= 21:
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
            for i in range(breakpoint - 20, breakpoint + 20):
                if i > -1 and i < player_num:
                    #the next year's score for the next people
                    temp_score = year_scores_dict[year][sorted_scores[i]]
                    #this is locating the incorrect score (idx is not correct atm)
                    if not numpy.isnan(temp_score):
                        close_scores_next_year.append(temp_score)

            chosen_influence = numpy.mean(close_scores_next_year) * 0.5 + corr * 0.5


        #greater than or equal to 5 years of experience
        else:
            chosen_influence = corr

        #Extrapolation and average part
        avg = averages[year]
        avg = last_year_score * (1 + avg) * 0.3
        chosen_influence *= 0.7
        next_year_score = chosen_influence + avg
        predictions.append([player, next_year_score, last_year_score])

    predictions = sorted(predictions, key=lambda x:x[1], reverse=True)
    last_year_rankings = sorted(predictions, key=lambda x:x[2], reverse=True)
    #assuming that the top 120 players of this year are within the top 200 players of last year
    player_rank_dictionary = defaultdict(list)
    for i in range(len(predictions)):
        player_rank_dictionary[predictions[i][0]].append(i)
    for i in range(len(predictions)):
        player_rank_dictionary[last_year_rankings[i][0]].append(i)
    for i in range(len(predictions)):
        placement = player_rank_dictionary[predictions[i][0]][1] - player_rank_dictionary[predictions[i][0]][0]
        player_rank_dictionary[predictions[i][0]].append(placement)
    
    rel_path3 = '../text_files/predictions.txt'
    abs_path = os.path.join(script_dir, rel_path3)
    f = open(abs_path, 'w')
    for i in predictions:
        entry = player_rank_dictionary[i[0]]
        f.write(i[0] + ',' + str(entry[0]) + ',' + str(entry[1]) + ',' + str(entry[2]) + '\n')
    f.close()
    return predictions, last_year_rankings

    #THINGS TO FIX
    #1. last_year_score plays too much of a role currently -> sort of fixed
    #2. extrapolation is garbage
    #3. we need some way to balance anomolous scores -> sort of fixed
