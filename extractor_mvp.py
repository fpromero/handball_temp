# -*- coding: utf-8 -*-
"""
Created on Tue Dec 31 08:16:22 2019

@author: FranciscoP.Romero

Player of the Match extractor
"""


import pandas as pd

headers = ['Match', 'Team','No.','Name', 'Role']

path = 'C:/Users/FranciscoP.Romero/Desktop/euro2020/'
match = '01'
team = ''
number = ''
values = []
rows_players = []
for i in range (1, 66): 
    match = (str(i) if (i >= 10) else ('0' + str(i)) )
    state = 0
    
    with open( path + match + '.csv') as f:
        for linea in f:
            if (linea.find('the Match') != -1):
                lin_sepl = linea.split(sep=',')
                # exttract team and number
                if lin_sepl[1] == '':
                    team = lin_sepl[2] 
                    number = lin_sepl[4]
                else: 
                    team = lin_sepl[1] 
                    number = lin_sepl[3]
                # extract name
                name = ''
                for l in lin_sepl[4:]:
                    if (l != '' and not l.isdigit()):
                        if (name == ''):
                            name += l.upper() + ' '
                        else:
                            name += l.strip()
                # role goalkeeper or field player
                role = 'FP' #if (name in goalkeepers) else 'FP'
                ## add file
                rows_players.append([match, team, number, name, role])
                

                    
import pandas as pd  
df_players = pd.DataFrame(rows_players, columns = headers ) 
df_players.set_index('Match', inplace = True)               
df_players.to_csv("euro2020_playersofthematch.csv")

