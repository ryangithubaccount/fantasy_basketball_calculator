import os
import numpy
from collections import defaultdict
from analysis_files.placement_to_string import placement_to_string

def predict_pattern(player_scores, player_score_change):
    script_dir = os.path.dirname(__file__)
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
            temp.append(player_scores.loc[i][j])
        year_scores_dict[i] = temp
        sorted_year_indices[i] = numpy.argsort(temp)


    #CALCULATING NEXT YEAR'S OUTPUT
    for index in range(len(active_players)):
        player = active_players[index][:-1]
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
            #weights the last two years if there is a significant drop or improvement in performance
            last_year_score = personal_scores[year - 1] * 0.6 + personal_scores[year - 2] * 0.4
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
                    #the next year's score for the closely correlated people
                    temp_score = year_scores_dict[year][sorted_scores[i]]
                    if not numpy.isnan(temp_score):
                        close_scores_next_year.append(temp_score)

            chosen_influence = numpy.mean(close_scores_next_year) * 0.5 + corr * 0.5


        else:
            chosen_influence = corr

        avg = averages[year]
        avg = last_year_score * (1 + avg) * 0.3
        chosen_influence *= 0.7
        next_year_score = chosen_influence + avg
        predictions.append([player, next_year_score, last_year_score])

    predictions = sorted(predictions, key=lambda x:x[1], reverse=True)
    last_year_rankings = sorted(predictions, key=lambda x:x[2], reverse=True)
    player_rank_dictionary = defaultdict(int)
    for i in range(len(predictions)):
        player_rank_dictionary[predictions[i][0]] -= i
        player_rank_dictionary[last_year_rankings[i][0]] += i
    #only need the first 120 players
    for i in range(120):
        placement = player_rank_dictionary[predictions[i][0]]
        predictions[i].append(placement)
    #we want to sort the top 120 players in next year's prediction by their placement gain/loss
    movement = sorted(predictions[:120], key=lambda x:x[3])
    top_gainers = movement[-1:-6:-1]
    top_losers = movement[:5]
    placement_to_string(120, predictions)
    placement_to_string(5, top_gainers)
    placement_to_string(5, top_losers)
    return predictions, last_year_rankings, top_gainers, top_losers