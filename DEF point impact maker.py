import requests
from bs4 import BeautifulSoup
import pandas as pan


def team_avg_ppg(team_abbreviation):
    url = 'https://www.pro-football-reference.com/teams/' + team_abbreviation + '/2022.htm'
    page = requests.get(url)

    soup = BeautifulSoup(page.text, 'lxml')
    table = soup.find('table', {'class': 'sortable stats_table', 'id': 'games'})

    underheaders = []
    for i in table.find_all('th', {'class': 'poptip'}):
        title = i.text.strip()
        underheaders.append(title)

    dataframe = pan.DataFrame(columns=underheaders[1:])

    for row in table.find_all('tr')[2:]:
        data = row.find_all('td')
        row_data = [td.text.strip() for td in data]

        length = len(dataframe)
        dataframe.loc[length] = row_data

    games_played = 0
    i = 0
    while i < len(dataframe.iloc[:, lambda df: [9]]):
        if dataframe.at[i, 'Tm'] != '':
            games_played += 1
        i += 1

    sznscore = 0
    i = 0
    while i < games_played:
        if dataframe.at[i, 'Tm'] != '':
            wkscore = int(dataframe.at[i, 'Tm'])
            sznscore += wkscore
        i += 1

    i = 0
    opponents_list = []
    pts_against_list = []
    while dataframe.at[i, 'Tm'] != '' or i < games_played:
        opponents_list.append(dataframe.iat[i, 8])
        pts_against_list.append(dataframe.iat[i, 10])
        i += 1

    print(opponents_list)
    print(pts_against_list)

    ppg_tm = sznscore / games_played
    print(team_abbreviation + str(ppg_tm))
    return ppg_tm


'''teams = ['crd', 'gnb', 'chi', 'buf', 'nwe', 'ram', 'sfo', 'dal', 'was', 'nyg', 'kan', 'sea', 'atl', 'car', 'cle',
         'nyj', 'pit', 'rai', 'oti', 'tam', 'rav', 'clt', 'mia', 'den', 'nor', 'phi', 'det', 'min', 'sdg', 'jax',
         'htx', 'cin']'''

def teams_played():
    '''url = 'https://www.pro-football-reference.com/teams/' + team_abbreviation + '/2022.htm'
    page = requests.get(url)

    soup = BeautifulSoup(page.text, 'lxml')
    table = soup.find('table', {'class': 'sortable stats_table', 'id': 'games'})

    underheaders = ' '
    for i in table.find_next('th', {'class': 'poptip'}):
        title = i.text.strip()
        underheaders.append(title)'''





team = input('Enter a teams abbreviation: ')
szn_ppg = team_avg_ppg(team_abbreviation=team)
print('Season avg for ' + team + ' is ' + str(round(szn_ppg, 2)))
