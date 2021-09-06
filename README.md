# <a href="fantasybasketballcalculator.pythonanywhere.com">Fantasy Basketball Calculator</a>
A math-based fantasy basketball project designed to generate predictions of next year's players.

## Functions and Usage
To clone repository:
```
git clone https://github.com/ryangithubaccount/fantasy_basketball_calculator.git
```
### Analysis Files
Access functions through
```
from analysis_files.file_name import function_name
```
#### score_calculator.py
1) calculate_score: Returns player fantasy scores based on their recorded stats (documentation under Calculation Details)
2) calculate_overall_scores: Calculates scores for every player that has played in the last 20 years. Returns a Pandas Dataframe mapping scores to players and years as well as a Pandas Dataframe recording score percent changes.
#### default_scorer.py
1) return_default: Returns a saved list of predictions generated on the default settings (to save calculation time)
#### pattern_calculator.py
1) predict_pattern: Calculates next year's fantasy score projections based on correlations and patterns (documentation under Calculation Details). Returns predictions, last year rankings, and players with the most movement in rankings.
#### placement_to_string.py
1) placement_to_string: Makes ranking movement more aesthetic. ie) '5' is converted to '+5' and '0' is converted to '~0'.

### Flask_app.py
The module responsible for running the web application 'fantasybasketballcalculator.pythonanywhere.com'. It renders HTML files stored in the templates/ folder and receives user input to determine what functions and files to execute.

### Templates
HTML files used in the web application 'fantasybasketballcalculator.pythonanywhere.com'. Their usage is monitored by 'flask_app.py'.

### Text Files
Text files that have saved data on them including player stats, default predictions, and a list of active player names.

### Stat Retrieval Files
These files are no longer actively used, but they provided the web scraping mechanisms to collect the player stats. Web scraping was accomplished through Beautiful Soup.


## Calculation Details
The calculations were based on NBA stats collected from BasketBall reference. To collect the data, the programs in stat_retrieval_files/ were used to web scrape
player stats from 2000 to present.

Players were assigned point scores based on their per-game fantasy totals as well as total season fantasy points. Fantasy points were determined by assigning
point values to the stats: points, three pointers made, field-goal attempts, field-goals made, free-throw attempts, free-throws made, rebounds, assists,
steals, blocks, and turnovers. Per-game averages for each player were extrapolated to an 82 game season. This value was given an 80% weight while the total season
fantasy points were given a 20% weight. This was used to incorporate player availability and durability into a player's value. A point score was assigned to every
year in a player's career to provide data trends on career progression.

To extrapolate next year's totals, each player's scores were converted to percent score change from year to year. Then, the Pandas 'correlation' function was used
to match similar player progressions. The top 100 matched correlations for each player were used to find a prediction of next year's percent change.

For players with less than 5 years in the league, an additional metric was taken since correlations were less reliable. The top 40 players who had the closest scores in their 'ith' year of playing to the player in question had their next year scores averaged. This 'mean score' provided an additional level of prediction
to the correlation.

Finally, the average percent progression for a player in each year of playing in the NBA was calculated. This league average was used to balance uncharacteristic
progression.

For players with 5 or more years in the league, their next-year score was calculated with a 70% weight to their correlation derived score and 30% to the league
average. For players with less than 5 years in the league, their next-year score was calculated with a 35% weight to the correlation derived score, 35% weight to
the mean score of similarly scoring players, and 30% weight to the league-average.

Since the progression was based on percent change from year to year, the calculations were based on a player's scoring from their most recent year in the league. 
However, for cases where there was significant drop or increase in performance (most likely due to anomalous situations such as injury or suspension) the last year
score was calculated with a 60% weight to the last year and 40% weight to the year before that.

## Implementation
These calculations were published in a web app at 'fantasybasketballcalculator.pythonanywhere.com'. The files for the web pages can be found in templates/ which holds a collection of HTML files. The functions and templates were rendered using 'flask_app.py'.

## Tools Used
Beautiful Soup, Pandas, Flask, and PythonAnywhere were all used to make the web app. They were used to web scrape, process data, and convert the original python
code into a workable app.
