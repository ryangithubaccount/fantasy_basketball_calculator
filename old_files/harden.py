#from selenium import webdriver
from bs4 import BeautifulSoup
import requests
from collections import defaultdict
import os


page = requests.get("https://www.basketball-reference.com/players/h/hardeja01.html")
soup = BeautifulSoup(page.content, 'html.parser')
stat_names = ['G', 'GS', 'MP', 'FG', 'FGA', 'FG%', '3P', '3PA', '3P%', '2P', '2PA', '2p%', 'EFG%', 'FT', 'FTA', 'FT%', 'ORB', 'DRB', 'TRB', 'AST', 'STL', 'BLK', 'TOV', 'PF', 'PTS']
years = ['2003', '2004', '2005', '2006', '2007', '2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015', '2016', '2017', '2018', '2019', '2020', '2021']
stat_dict = defaultdict(list)
for i in range(1, 26):
    stat_dict[i] += [stat_names[i - 1]]

script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
rel_path = "text_files/harden_stats.txt"
abs_file_path = os.path.join(script_dir, rel_path)
f = open(abs_file_path, 'w')

name = soup.find('h1', itemprop='name')
f.write(name.get_text())
first_year = soup.find('tr', class_='full_table').find(class_='left').get_text()[0:4]
f.write(first_year + '\n')

for year in years:
    total = soup.find(id='per_game.' + year, class_='full_table')
    if total:
        f.write(year + ': ')
        stat_dict[0] += [year]
        stats = total.find_all(class_='right')
        #25 items
        for i in range(1, 26):
            stat_dict[i] += [stats[i - 1].get_text()]
            f.write(stats[i - 1].get_text() + ' ')
        f.write('\n')




