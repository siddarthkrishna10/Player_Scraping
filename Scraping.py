import csv
import requests
from bs4 import BeautifulSoup

url = "https://footballapi.pulselive.com/football/stats/ranked/players/goals?page={}&pageSize=20&comps=1&compCodeForActivePlayer=EN_PR&altIds=true"

headers = {
    'Origin': 'https://www.premierleague.com',
}

def get_items(link,page):
    while True:
        res = requests.get(link.format(page),headers=headers)
        soup = BeautifulSoup(res.text,"lxml")
        if not len(res.json()['stats']['content']):break
        for item in res.json()['stats']['content']:
            player_name = item['owner']['name']['display']
            goals = item["value"]
            rank = item["rank"]
            yield rank, player_name, goals

        page+=1

if __name__ == '__main__':
    page = 0
    with open("Player_info.csv","w", newline="") as outfile:
        writer = csv.writer(outfile)
        writer.writerow(['Rank','Player','Goals'])
        for name in get_items(url,page):
            writer.writerow(name)

fieldnames = ("Rank","Player","Goals")
with open('player_info.csv', 'r') as csvFile:
    reader = csv.DictReader(csvFile, fieldnames)
    csv_data = list(reader)

with open('player_info.json', 'w') as jsonFile:
    json.dump(csv_data, jsonFile, indent=4)
