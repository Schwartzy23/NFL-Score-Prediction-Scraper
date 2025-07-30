import requests
from bs4 import BeautifulSoup
import pandas as pan


def obtain_data(team_abbreviation, year):
    url = 'https://www.pro-football-reference.com/teams/' + team_abbreviation + '/' + year + '.htm'
    page = requests.get(url)

    soup = BeautifulSoup(page.text, 'lxml')
    table = soup.find('table', {'class': 'sortable stats_table', 'id': 'games'})

    overheaders = []
    for i in table.find_all('th', {'class': 'over_header'}):
        title = i.text.strip()
        overheaders.append(title)

    underheaders = []
    for i in table.find_all('th', {'class': 'poptip'}):
        title = i.text.strip()
        underheaders.append(title)

    dataframe = pan.DataFrame(columns=underheaders)

    for row in table.find_all('tr')[2:]:
        week = row.find_next('th')
        wknum = week.text.strip()

        data = row.find_all('td')
        row_data = [td.text.strip() for td in data]
        row_data.insert(0, wknum)

        length = len(dataframe)
        dataframe.loc[length] = row_data

    dataframe.to_excel('Aidan.xlsx')

    TM_PTS_LOC = 10




    games_played = 0
    i = 0
    while i < len(dataframe.iloc[:, lambda df: [10]]):
        if dataframe.at[i, 'Tm'] == '':
            i += 1
        else:
            games_played += 1
            i += 1
    # print(games_played)
    # print(season_pts_scored_tm)
    print('Games played in ' + year + ': ' + str(games_played))

    sznscore = 0
    i = 0
    while i < games_played:
        if dataframe.at[i, 'Tm'] == '':
            i += 1
        else:
            wkscore = int(dataframe.at[i, 'Tm'])
            sznscore += wkscore
            i += 1
        # print(sznscore)

    # print(sznscore)
    ppg_tm = sznscore / games_played

    return ppg_tm


years = [2020, 2021, 2022]
chosen_team = input('Enter team abbreviation: ')
for current_year in years:
    szn_ppg = obtain_data(team_abbreviation=chosen_team, year=str(current_year))
    print('Season avg ppg: ' + str(round(szn_ppg, 2)))

    '''teams = ['crd', 'gnb', 'chi', 'buf', 'nwe', 'ram', 'sfo', 'dal', 'was', 'nyg', 'kan', 'sea', 'atl', 'car', 'cle',
             'nyj', 'pit', 'rai', 'oti', 'tam', 'rav', 'clt', 'mia', 'den', 'nor', 'phi', 'det', 'min', 'sdg', 'jax',
             'htx', 'cin']'''


