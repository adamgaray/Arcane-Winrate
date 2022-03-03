import tweepy
import os
import requests
from credentials import *
from bs4 import BeautifulSoup

def get_tweet():
    URLS = ['https://lol.fandom.com/wiki/LEC/2022_Season/Spring_Season/Champion_Statistics', \
        'https://lol.fandom.com/wiki/LCK/2022_Season/Spring_Season/Champion_Statistics', \
        'https://lol.fandom.com/wiki/LCS/2022_Season/Spring_Season/Champion_Statistics', \
        'https://lol.fandom.com/wiki/LPL/2022_Season/Spring_Season/Champion_Statistics']
    ARCANE = ['Vi', 'Jinx', 'Ekko', 'Singed', 'Caitlyn', 'Jayce', 'Heimerdinger', 'Viktor']

    rates = [[], [], []]                                                                                # [[champs], [# games played], [# wins]]

    for url in URLS:
        page = requests.get(url).text
        soup = BeautifulSoup(page, 'html.parser')

        # tables = soup.find_all('table')                                                               # to find all tables from url and determine correct class_
        table = soup.find('table', class_='wikitable sortable spstats plainlinks hoverable-rows')
    
        skip = 0
        for row in table.tbody.find_all('tr'):
            
            if (skip < 5):                                                                              # skip header rows
                skip += 1
                continue

            columns = row.find_all('td')

            champ = columns[0].text.strip()                                                             # get champ, games, winrate
            if (champ not in ARCANE): continue
            gp = int( columns[4].text.strip() )
            w = int( columns[6].text.strip() )

            if (champ not in rates[0]):                                                                 # add to rates
                rates[0].append(champ)
                rates[1].append(gp)
                rates[2].append(w)
            else:
                index = rates[0].index(champ)
                rates[1][index] += gp
                rates[2][index] += w

    winrate = (sum(rates[2]) / sum(rates[1])) * 100                                                     # calculate winrate
    return "Arcane champion winrate is {:.2f}% BatChest".format(winrate)

def lambda_handler(event, context):
    print("Get credentials")

    print("Authenticate")
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth)

    print("Calculate winrate and get tweet")
    tweet = get_tweet()

    print(f"Post tweet: {tweet}")
    api.update_status(tweet)

    return {"statusCode": 200, "tweet": tweet}

if __name__ == "__main__":
    lambda_handler(event=None, context=None)
