import requests
from bs4 import BeautifulSoup
import json
import pandas as pd
import time

url = 'https://store.steampowered.com/search/results/?query&start=0&count=50&dynamic_data=&sort_by=_ASC&snr=1_7_7_7000_7&filter=topsellers&infinite=1'

def total_results(url):
    r = requests.get(url)
    data = dict(r.json())
    total_results = data['total_count']
    return int(total_results)

def get_data(url):
    r = requests.get(url)
    data = dict(r.json())
    return data['results_html']

def parse(data):
    games_list = []
    soup = BeautifulSoup(data, 'html.parser')
    games = soup.find_all('a')
    for game in games:
        title = game.find('span', {'class': 'title'}).text
        price = game.find('div', {'class': 'search_price'}).text.strip().split('Rp')[1]
        try:
            disc_price = game.find('div', {'class': 'search_price'}).text.strip().split('Rp')[2]
        except:
            disc_price = price

        my_games = {
            'title': title,
            'price': price,
            'disc_price': disc_price
        }
        games_list.append(my_games)
    return games_list

def output(results):
    gamesdf = pd.concat([pd.DataFrame(g) for g in results])
    gamesdf.to_csv('games-prices.csv', index=False)
    print('Saved to CSV')
    print(gamesdf.head())
    return

results = []
for x in range(0, total_results(url), 50):
    data = get_data(f'https://store.steampowered.com/search/results/?query&start={x}&count=50&dynamic_data=&sort_by=_ASC&snr=1_7_7_7000_7&filter=topsellers&infinite=1')
    results.append(parse(data))
    print('Results Scrapped: ', x)
    time.sleep(1.5)

output(results)