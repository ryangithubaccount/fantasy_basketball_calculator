# fantasy_basketball_calculator
A math-based fantasy basketball project designed to generate predictions of next year's players.

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
These calculations were published in a web app at 'fantasybasketballcalculator.pythonanywhere.com'. The files for the web pages can be found in templates/ which holds a collection of html files. The functions and templates were rendered using 'flask_app.py'.

## Tools Used
Beautiful Soup, Pandas, Flask, and pythonanywhere were all used to make the web app. They were used to web-scrape, process data, and convert the original python
code into a workable app.
