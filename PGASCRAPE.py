import json
import requests
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from pymongo import MongoClient

# Construct the connection string with the correct credentials
username = "elilowe321"
password = "Th0rbr0ver12"
connection_string = f"mongodb+srv://elilowe321:Th0rbr0ver12@golfsim.elk3ata.mongodb.net/"

client = MongoClient(connection_string)
db = client['bet_db']
mycol = db["players"]

#This is player obj for day 1-4
"""
class player:

    def __init__(self):
        self.name = None
        self.score = None
        self.r1 = None
        self.r2 = None
        self.r3 = None
        self.r4 = None
        self.id = None

    #Print out obj
    def __str__(self):
        return f"player(name={self.name} )"

    #Getter methods
    def get_name(self):
        return self.name
    def get_score(self):
        return self.score
    def get_r1(self):
        return self.r1
    def get_r2(self):
        return self.r2
    def get_r3(self):
        return self.r3
    def get_r4(self):
        return self.r4
    def get_id(self):
        return self.id

    #Setter methods
    def name(self, value):
        self.name = value
    def score(self, value):
        self.score = value
    def weight(self, value):
        self.weight = value
    def r1(self, value):
        self.r1 = value
    def r2(self, value):
        self.r2 = value
    def r3(self, value):
        self.r3 = value
    def r4(self, value):
        self.r4 = value
    def id(self, value):
        self.id = value
"""

#Player obj for tour data (projected winner type stuff)
class player:
    def __init__(self):
        self.id = None
        self.name = None
        self.first_name = None
        self.last_name = None
        self.stats = []

    # Print out obj including stats
    def __str__(self):
        return f"Player(name={self.name}, stats={self.stats})"

    # Getter methods
    def get_id(self):
        return self.id

    def get_name(self):
        return self.name

    def get_first_name(self):
        return self.first_name

    def get_last_name(self):
        return self.last_name

    def get_stats(self):
        return self.stats

    # Setter methods
    def set_id(self, value):
        self.id = value

    def set_name(self, value):
        self.name = value

    def set_first_name(self, value):
        self.first_name = value

    def set_last_name(self, value):
        self.last_name = value

    def add_stat(self, stat):
        self.stats.append(stat)

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

#Get leaderboad through espn scaping
#url = 'https://www.espn.com/golf/leaderboard'
url = 'https://www.espn.com/golf/leaderboard/_/tournamentId/401465533'
response = requests.get(url)
html = response.text
soup = BeautifulSoup(html, 'html.parser')
dfs = pd.read_html(url, header = 0)
data = dfs[-1]

#loop through and add player to array
espn_players = []
for index, row in data.iterrows():
    
    #Get Everyone Before the cut then stops (Good for last 2 days)
    player_data = player()

    if(len(row["PLAYER"].split()) >= 3):
        player_data.first_name = ' '.join(row["PLAYER"].split()[:2])
        player_data.last_name = row["PLAYER"].split()[-1]
    else:
        player_data.first_name = row['PLAYER'].split()[0]
        player_data.last_name = row['PLAYER'].split()[1]
       
    player_data.name = f"{player_data.first_name} {player_data.last_name}"
    player_data.score = row['SCORE']
    player_data.r1 = row['R1']
    player_data.r2 = row['R2']
    player_data.r3 = row['R3']
    player_data.r4 = row['R4']
    
    if(player_data.score == "CUT"):
        break    
    
    espn_players.append(player_data)


# Send a GET request to the players page
response = requests.get("https://www.pgatour.com/players")

if response.status_code == 200:
    # Create BeautifulSoup object from the HTML content
    soup = BeautifulSoup(response.content, 'html.parser')
    script_tag = soup.find("script", id="__NEXT_DATA__")
    if script_tag:
        # Extract the JSON data from the script tag
        json_data = script_tag.string

        # Parse the JSON data
        data = json.loads(json_data)

        # Access the player information
        tour_players = data["props"]["pageProps"]["players"]["players"]
        
        # Create a dictionary to store the ESPN player names as keys for faster complexity
        espn_names_dict = {player.name: player for player in espn_players}  

        #Loop through tour players and get ID to scrape stats
        db_players = []
        count = 0
        for i in tour_players:
            if count > 10:
                break
            if i["displayName"] in espn_names_dict:
                count+=1

                # Create a WebDriver instance with the Chrome options
                driver = webdriver.Chrome()

                # Navigate to the desired URL
                driver.get(f"https://www.pgatour.com/player/{i['id']}/{i['firstName']}-{i['lastName']}/stats")

                # Get the page source
                # Wait for the element to be present
                try:
                    wait = WebDriverWait(driver, 10)  # Wait for a maximum of 10 seconds
                    element = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="tabs-:rf:--tabpanel-4"]/div/div/div[3]/div[2]/div[6]/div/div[2]/div/div/table')))

                    data = element.text
                    lines = data.split('\n')

                    player_data = player()
                    player_data.id = i['id']
                    player_data.name = i['displayName']
                    player_data.first_name = i['firstName']
                    player_data.last_name = i['lastName']
                    for i in range(5, len(lines)):
                        if i + 3 < len(lines):  # Check if there are enough lines available

                            # Check if the next line contains a bracket
                            if lines[i].startswith('(') or lines[i+1].startswith('(') or lines[i+2].startswith('(') or lines[i+3].startswith('('):
                                i += 3  # Skip the current line and the next line
                            else:

                                if not is_number(lines[i]) and '%' not in lines[i] and '-' not in lines[i]:
                                    stat = {
                                        'STAT': lines[i].strip(),
                                        'VALUE': lines[i+1].strip() if lines[i+1] != '-' else 'No Value',
                                        'RANK': lines[i+2].strip() if lines[i+2] != '-' else 'Unranked'
                                    }
                                    player_data.stats.append(stat)

                    db_players.append(vars(player_data))  
                    driver.quit()
                except TimeoutException as ex:
                    print("TimeoutException occurred:", ex)
                    continue


        result = mycol.insert_many(db_players)

