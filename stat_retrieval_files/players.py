from bs4 import BeautifulSoup
import requests
from collections import defaultdict
import requests_cache
import os

requests_cache.install_cache()
website_name = 'https://www.basketball-reference.com'
page = requests.get(website_name + '/players')
soup = BeautifulSoup(page.content, 'html.parser')

alphabet = 'abcdefghijklmnopqrstuvwyz'
active_players = []

for i in alphabet:
    link = website_name + '/players/' + i
    page2 = requests.get(link)
    soup2 = BeautifulSoup(page2.content, 'html.parser')
    bold = soup2.find_all('tr')
    for i in bold:
        year = i.find_all('td')
        if year and year[1].get_text()[0:2] == '20':
            active = i.find(href = True)
            if active:
                active_players.append(active['href'])

#print(active_players)

script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
rel_path = "../text_files/player_stats.txt"
abs_file_path = os.path.join(script_dir, rel_path)
f = open(abs_file_path, 'w')

stat_names = ['G', 'GS', 'MP', 'FG', 'FGA', 'FG%', '3P', '3PA', '3P%', '2P', '2PA', '2p%', 'EFG%', 'FT', 'FTA', 'FT%', 'ORB', 'DRB', 'TRB', 'AST', 'STL', 'BLK', 'TOV', 'PF', 'PTS']
years = ['2000', '2001', '2002', '2003', '2004', '2005', '2006', '2007', '2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015', '2016', '2017', '2018', '2019', '2020', '2021']
for player in active_players:
    player_page = requests.get(website_name + player)
    player_soup = BeautifulSoup(player_page.content, 'html.parser')
    name = player_soup.find('h1', itemprop='name')
    f.write(name.get_text())
    first_year = player_soup.find('tr', class_='full_table').find(class_='left').get_text()[0:4]
    f.write(first_year + '\n')

    for year in years:
        total = player_soup.find(id='per_game.' + year, class_='full_table')
        if total:
            f.write(year + ': ')
            stats = total.find_all(class_='right')
            #25 items
            for i in range(1, 26):
                val = stats[i - 1].get_text()
                if not val:
                    f.write('na ')
                else:
                    f.write(stats[i - 1].get_text() + ' ')
            f.write('\n')
f.close()