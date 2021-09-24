import requests
import statistics as st
from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import norm
import numpy as np
import math
from datetime import datetime
import time

STAT_TYPES = ['PTS','AST', 'STL', 'TRB', 'FG%', '3P%', 'FT%', 'BLK']

#inputs:
#2 players: Name and year range they played in
#Stat type being compared(PTS,AST,REB, etc.)
#Comparing each player's career stats to the stats of other players in their career era
#Calculates Z score for each player and produces graphhical output
#Player with the higher z zcore is concidered better

#Main function containing user interface and instantian of player objects
def main():
    print_menu()

    while True:
        TYPE = input('Enter Stat Type to Compare: ')
        if TYPE in STAT_TYPES:
            break
        else:
            print("Invalid Stat Type")
    print_menu()

    p1_first_name = input('Enter P1 First Name: ')
    print_menu()
    p1_last_name = input('Enter P1 Last Name: ')
    
    print_menu()
    
    while True:
        while True: 
            p1_FY = input('Enter P1 First Year: ')
            try:
                p1_FY = int(p1_FY)
                break
            except TypeError:
                print('Invalid Input') 
            except ValueError:
                print('Invalid Input')      
        print_menu()

        while True: 
            p1_LY = input('Enter P1 Last Year: ')
            try:
                p1_LY = int(p1_LY)
                break
            except TypeError:
                print('Invalid Input') 
            except ValueError:
                print('Invalid Input')
        
        if(p1_FY >1950 and p1_FY <= datetime.now().year and p1_LY >1950 and p1_LY <= datetime.now().year and p1_LY >= p1_FY):
            break
        else:
            print_menu()
            print('Invalid Year Range')
    print_menu()

    p2_first_name = input('Enter P2 First Name: ')
    print_menu()
    p2_last_name = input('Enter P2 Last Name: ')
    
    print_menu()
    
    while True:
        while True: 
            p2_FY = input('Enter P2 First Year: ')
            try:
                p2_FY = int(p2_FY)
                break
            except TypeError:
                print('Invalid Input') 
            except ValueError:
                print('Invalid Input')      
        print_menu()

        while True: 
            p2_LY = input('Enter P2 Last Year: ')
            try:
                p2_LY = int(p2_LY)
                break
            except TypeError:
                print('Invalid Input') 
            except ValueError:
                print('Invalid Input')
        
        if(p2_FY >1950 and p2_FY <= datetime.now().year and p2_LY >1950 and p2_LY <= datetime.now().year and p2_LY >= p2_FY):
            break
        else:
            print_menu()
            print('Invalid Year Range')

    #instantiation of player objects

    P1 = Player(p1_first_name,p1_last_name,p1_FY,p1_LY, TYPE)
    P2 = Player(p2_first_name,p2_last_name,p2_FY,p2_LY, TYPE)
    
    print(compare_z_scores(P1, P2))
    plot_z_score(P1, 'p1')
    plot_z_score(P2, 'p2')


def clear():
    print('\n'*30)

#prints menu screen
def print_menu():
    clear()
    print('--------------------WELCOME TO NBA PLAYER ERAS--------------------')
    print('Stat Types: PTS, AST, STL TRB, FG%, 3P%, FT%, BLK') 
    print('\n'*10)
    time.sleep(.5)

#screen scrapes player career stats from player page on basketball-reference.com
#stores in Pandas Data Frame
#Cited from https://towardsdatascience.com/web-scraping-nba-stats-4b4f8c525994
def get_data(url):
    html = requests.get(url)
    soup = BeautifulSoup(html.content,'html.parser')
    # use findALL() to get the column headers
    soup.findAll('tr', limit=2)
    # use getText()to extract the text we need into a list
    headers = [th.getText() for th in soup.findAll('tr', limit=2)[0].findAll('th')]
    # exclude the first column as we will not need the ranking order from Basketball Reference for the analysis
    headers = headers[1:]

    # avoid the first header row
    rows = soup.findAll('tr')[1:]
    player_stats = [[td.getText() for td in rows[i].findAll('td')]
            for i in range(len(rows))]

    return pd.DataFrame(player_stats, columns = headers)


class Player:
    first_name = ''
    last_name = ''
    year_f = 0
    year_l = 0
    stats = pd.DataFrame()
    stat_type = ''
    mean = 0
    std = 0
    years_mean = 0
    years_std = 0

    #constructor method
    def __init__(self, first, last, year_f, year_l, stat_t):
        self.first_name = first.capitalize()
        self.last_name = last.capitalize()
        
        if stat_t in STAT_TYPES:
            self.stat_type = stat_t

        if(year_f >1950 and year_f <= datetime.now().year):
            self.year_f = year_f
        if(year_l >1950 and year_l <= datetime.now().year and year_l > year_f):
            self.year_l = year_l
        
        #formats basketball reference URL with player name
        def format_url():
            url = 'https://www.basketball-reference.com/players/'
            path = '{}/{}{}0{}.html' 
            path = path.format(self.last_name[0].lower(),self.last_name[:5].lower(),self.first_name[:2].lower(),str(1))
            url += path
            return url

        self.stats = get_data(format_url())

        #gets stat type data from data frame
        def get_col_data(data,type):
            years = 0
            arr = []
            for num in data['Age']:
                if num != None and num != '':
                    years +=1
            
            for i in range(0,years): 
                if data[type][i] != '' and data[type][i] != None:
                    arr.append(float(data[type][i]))
            
            return arr

        col_data = get_col_data(self.stats, self.stat_type)

        self.mean = st.mean(col_data)
        self.std = st.stdev(col_data)
    
    
    def get_year_averages(self,year):
        #calculates stat average for specific year
        url = 'https://www.basketball-reference.com/leagues/NBA_{}_per_game.html'.format(year)
        stats = get_data(url)[self.stat_type]

        #converts data to list
        arr = []
        for num in stats:
            if num != None and num != '':
                arr.append(float(num))
        #returns list containing mean and standard deviation of season averages
        mean_sd = []
        mean_sd.append(st.mean(arr))
        mean_sd.append(st.pstdev(arr))
        return mean_sd

    #calculates average stat type for entered year range
    def decade_averages(self):
        current_year = self.year_f
        y_means = []
        y_stdevs = []
        while current_year <= self.year_l:
            year_stats = self.get_year_averages(current_year)
            y_means.append(year_stats[0])
            y_stdevs.append(year_stats[1])
            current_year +=1
        self.years_mean = st.mean(y_means)
        self.years_std = st.mean(y_stdevs)
        return 0

#calculates z-score
def calc_z_score(x, mu, sigma):
    return (x-mu)/sigma


#compares both player z scores and decides who is better (larger z score)
def compare_z_scores(p1, p2):
    if p1.decade_averages() or p2.decade_averages() != 0:
        print('Calculation Error Exiting')
        exit(1)  
    p1_z = calc_z_score(p1.mean,p1.years_mean,p1.years_std)
    p2_z = calc_z_score(p2.mean,p2.years_mean,p2.years_std)
    message = '{} {} with a z-score of {} is better than {} {} with a z-score of {} when comparing {}'
    if p1_z > p2_z:
        message = message.format(p1.first_name, p1.last_name, round(p1_z,3), p2.first_name, p2.last_name, round(p2_z,3), p1.stat_type)
    elif p2_z > p1_z:
        message = message.format(p2.first_name, p2.last_name, round(p2_z,3), p1.first_name, p1.last_name, round(p1_z,2), p1.stat_type)
    else:
        message = 'Both players have the same z-score so they are equally as good'
    return message


#Graphs where player lies on normal curve compared to their decade
def plot_z_score(player, file_name):
    domain = np.linspace(player.years_mean - 3*player.years_std,player.years_mean + 4*player.years_std,1000)
    plt.plot(domain, norm.pdf(domain,player.years_mean,player.years_std))
    plt.title("NBA {} Distribution\n{} - {}".format(player.stat_type, str(player.year_f), str(player.year_l)))
    plt.xlabel('{}'.format(player.stat_type), fontsize = 12)
    plt.ylabel('Density', fontsize = 12)
    plt.vlines(player.mean,0,.1, colors = 'Red', label = player.first_name.capitalize(), linestyles = 'dashed' )
    plt.text(player.mean,0.1,player.last_name.capitalize()+ '\nμ = '+str(round(player.mean,3))+'\nσ = '+str(round(player.std, 3)), color = 'Red', fontsize = 13)
    plt.fill_between(domain, 0, norm.pdf(domain, player.years_mean, player.years_std))
    plt.savefig('{}.png'.format(file_name))
    plt.close()

if __name__ == '__main__':
    main()