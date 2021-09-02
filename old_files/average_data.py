import os
import pandas as pd
import numpy
import matplotlib.pyplot as plt

script_dir = os.path.dirname(__file__)
rel_path = 'csv_files/player_score_changes.csv'
abs_file_path = os.path.join(script_dir, rel_path)

player_score_change = pd.read_csv(abs_file_path)
averages = player_score_change.mean(axis='columns')
averages.plot()
plt.show()
#slope before that is ~ (-0.17333)
#slope after 4 years is ~ (-0.0235)
