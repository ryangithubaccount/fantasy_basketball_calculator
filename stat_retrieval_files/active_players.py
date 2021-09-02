from bs4 import BeautifulSoup
import requests
from collections import defaultdict
import requests_cache
import os

requests_cache.install_cache()
website_name = 'https://www.basketball-reference.com'
page = requests.get(website_name + '/players')
soup = BeautifulSoup(page.content, 'html.parser')

script_dir = os.path.dirname(__file__)
rel_path = '../text_files/active_players.txt'
abs_file_path = os.path.join(script_dir, rel_path)

f = open(abs_file_path, 'w')
alphabet = 'abcdefghijklmnopqrstuvwyz'
active_players = []
for i in alphabet:
    link = website_name + '/players/' + i
    page2 = requests.get(link)
    soup2 = BeautifulSoup(page2.content, 'html.parser')
    bold = soup2.find_all('strong')
    for player in bold:
        player = player.find(href = True)
        if player:
            page2 = requests.get(website_name + player['href'])
            soup2 = BeautifulSoup(page2.content, 'html.parser')
            name = soup2.find('h1', itemprop='name')
            f.write(name.get_text()[1:])
f.close()
