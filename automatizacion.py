# -*- coding: utf-8 -*-
"""
Created on Tue May  5 07:25:01 2020

@author: FranciscoP.Romero
"""

import pandas as pd
import numpy as np
import math

data_path = "C:/Users/FranciscoP.Romero/Desktop/BERABERA/"
file_name = "berabera-elche"
df = pd.read_csv(data_path + file_name + ".csv", sep="\t")
teams = df["Equipo"].unique()
match = df["Partido"].unique()[0]
# local y visitante
pos_0 = match.find(teams[0])
pos_1 = match.find(teams[1])
if (pos_1 == -1 or (pos_0 != -1 and pos_0 < pos_1)):
    local_team = teams[0]
    visit_team = teams[1]
else: 
    local_team = teams[1]
    visit_team = teams[0]


##
# DICCIONARIOS
##

columns_out = ["Match", "Team", "Player", "Role", "Score", "Score5",
               "9mGoal",   "9mSave", "9mOut", "9mBlock",
               "6mGoal", "6mSave", "6mOut",
               "FBGoal" ,  "FBSave", "FBOut",
               "7mGoal", "7mSave", "7mOut",
               "Assist", "Received7m", "Provoke2m", "Steal","GoodDef", "Block",
               "Turnover", "DefMistake",  "2mJ", "2mBB", "RedBlueCard"
               ]

w = [1.5, -0.75, -1, -1,
           1, -0.7, -0.8,
           1, -1.5, -1.5, 
           1, -1.3, -1.3,
           0.5, 1, 0.8, 1, 0.8, 0.8,
           -0.8, -0.8, -0.8, -2, -2
           ]

w_gk = [-1, 1, 0.5, 0.5,
           -0.6, 1.5, 1,
           -0.5, 1.5, 1.5, 
           -0.4, 1.5, 1.5,
           0.85, 1, 0.8, 1, 0, 0,
           -0.8, -0.8, -0.8, -2, -2
           ]


dict_acc = {"Asistencia":"Assist", "Buena Defensa": "GoodDef", 
            "Error Defensa": "DefMistake", "Provoca 2'": "Provoke2m",
            "Blocaje": "Block", "Recuperacion": "Steal", "Recibe 7m": "Received7m"}



df_out = pd.DataFrame(columns= columns_out)


## 
# FUNCIONES
## 
def truncate(numero, cifras = 1):
    posiciones = pow(10.0, cifras)
    return math.trunc(posiciones * numero) / posiciones

def create_row(match, team, player, role, columns):
    row_data = [match, team, player, role] 
    row_data = row_data + ([0] * (len(columns)- len(row_data)))
    return pd.DataFrame([row_data], columns= columns)


def detect_scoring_actions(actions, match, team, df_out):
    for act in actions:
        a_lst = act.split(",")
        for a in a_lst:
            pos = a.find(":")
            player =  a[: pos].strip()
            accion = a[pos + 1: ]
            ## borrar etiquetado ocasional
            accion = accion.strip("[")
            accion = accion.strip("]")
            col = dict_acc.get(accion)
            if (df_out[df_out.Player == player].shape[0] == 0):
                df_out_aux=create_row(match,team, player, "FP", columns_out)
                df_out = pd.concat([df_out_aux, df_out], sort = True)
            # contar jugada
            df_out.loc[df_out['Player']== player, col] +=1
    return df_out



def register_action(df, col, role, df_out):
    for i, f in df.iterrows():
        player = f['Jugador/a'].strip()
        if (df_out[df_out.Player == player].shape[0] == 0):
            df_out_aux=create_row(f['Partido'],f['Equipo'],player, role, columns_out)
            df_out = pd.concat([df_out_aux, df_out], sort = True)
        df_out.loc[df_out['Player'] == player , col] += 1
    return df_out


#Goals
dfGoal= df[['Partido','Equipo', 'Jugador/a', 'Zona Accion', 'Portero/a']][df.Posesion=="[Acierto]/[Gol]"]
#9mGoal
actions = [["9mGoal", "[9m]"],["6mGoal", "[6m]"], ["FBGoal", "[CT]"], ["7mGoal", "7m"]]
for a in actions:
    col = a[0]
    dfActGoal = dfGoal[dfGoal["Zona Accion"].str.startswith(a[1])]
    #player 
    dfActGoal_players = dfActGoal.groupby(['Partido','Equipo', 'Jugador/a'])['Partido','Equipo', 'Jugador/a'].size().reset_index(name='counts')
    for i, f in dfActGoal_players.iterrows():
        player = f['Jugador/a'].strip()
        if (df_out[df_out.Player == player].shape[0] == 0):
            df_out_aux=create_row(f['Partido'],f['Equipo'],player, "FP", columns_out)
    #df_out_aux = pd.DataFrame([[f['Partido'], f['Equipo'], f['Jugador/a']],0], columns=columns)
            df_out = pd.concat([df_out_aux, df_out])
        df_out.loc[df_out['Player']== player , col] = f['counts']
    # goalkeeper
    dfActGoal_gk = dfActGoal.groupby(['Partido','Equipo','Portero/a'])['Partido','Equipo','Portero/a'].size().reset_index(name='counts')
    for i, f in dfActGoal_gk.iterrows():
        if (f['Portero/a'] != "NINGUNO"):
            if (df_out[df_out.Player == f['Portero/a']].shape[0] == 0):
                team = teams[1] if f['Equipo'] == teams[0] else teams[0]
                df_out_aux=create_row(f['Partido'],team,f['Portero/a'], "GK", columns_out)
                df_out = pd.concat([df_out_aux, df_out])
            df_out.loc[df_out['Player']==f['Portero/a'] , col] = f['counts']
    
    
    
# Paradas
dfSave = df[df.Posesion == "[Error]/[Parada]"]
actions_save = [["9mSave", "[9m]"],["6mSave", "[6m]"], ["FBSave", "[CT]"], ["7mSave", "7m"]]
for a in actions_save:
    col = a[0]
    dfSaveAct = dfSave[dfSave["Zona Accion"].str.startswith(a[1])]
    df_players = dfSaveAct.groupby(['Partido','Equipo', 'Jugador/a'])['Partido','Equipo', 'Jugador/a'].size().reset_index(name='counts')
    for i, f in df_players.iterrows():
        player = f['Jugador/a'].strip()
        if (df_out[df_out.Player == player].shape[0] == 0):
            df_out_aux=create_row(f['Partido'],f['Equipo'],player, "FP", columns_out)
            df_out = pd.concat([df_out_aux, df_out], sort = True)
        df_out.loc[df_out['Player']== player , col] = f['counts']
    # goalkeeper
    df_gk = dfSaveAct.groupby(['Partido','Equipo','Portero/a'])['Partido','Equipo','Portero/a'].size().reset_index(name='counts')
    for i, f in df_gk.iterrows():
        if (f['Portero/a'] != "NINGUNO"):
            if (df_out[df_out.Player == f['Portero/a']].shape[0] == 0):
                team = teams[1] if f['Equipo'] == teams[0] else teams[0]
                df_out_aux=create_row(f['Partido'],team,f['Portero/a'], "GK", columns_out)
                df_out = pd.concat([df_out_aux, df_out], sort = True)
            df_out.loc[df_out['Player']==f['Portero/a'] , col] = f['counts']

# Out
dfOut = df[df.Posesion == "[Error]/[Fuera]"]
actions_out = [["9mOut", "[9m]"],["6mOut", "[6m]"], ["FBOut", "[CT]"], ["7mOut", "7m"]]
for a in actions_out:
    col = a[0]
    dfOutAct = dfOut[dfOut["Zona Accion"].str.startswith(a[1])]
    df_players = dfOutAct.groupby(['Partido','Equipo', 'Jugador/a'])['Partido','Equipo', 'Jugador/a'].size().reset_index(name='counts')
    for i, f in df_players.iterrows():
        player = f['Jugador/a'].strip()
        if (df_out[df_out.Player == player].shape[0] == 0):
            df_out_aux=create_row(f['Partido'],f['Equipo'],player, "FP", columns_out)
            df_out = pd.concat([df_out_aux, df_out], sort = True)
        df_out.loc[df_out['Player']==player , col] = f['counts']
    # goalkeeper
    df_gk = dfOutAct.groupby(['Partido','Equipo','Portero/a'])['Partido','Equipo','Portero/a'].size().reset_index(name='counts')
    for i, f in df_gk.iterrows():
        if (f['Portero/a'] != "NINGUNO"):
            if (df_out[df_out.Player == f['Portero/a']].shape[0] == 0):
                team = teams[1] if f['Equipo'] == teams[0] else teams[0]
                df_out_aux=create_row(f['Partido'],team,f['Portero/a'], "GK", columns_out)
                df_out = pd.concat([df_out_aux, df_out], sort = True)
            df_out.loc[df_out['Player']==f['Portero/a'] , col] = f['counts']

df_pos = df[df.Posesion == "[Error]/[Blocaje]"]
actions_out = [["9mBlock", "[9m]"]]
for a in actions_out:
    col = a[0]
    df_act = df_pos[df_pos["Zona Accion"].str.startswith(a[1])]
    df_players = df_act.groupby(['Partido','Equipo', 'Jugador/a'])['Partido','Equipo', 'Jugador/a'].size().reset_index(name='counts')
    for i, f in df_players.iterrows():
        player = f['Jugador/a'].strip()
        if (df_out[df_out.Player == player].shape[0] == 0):
            df_out_aux=create_row(f['Partido'],f['Equipo'],player, "FP", columns_out)
            df_out = pd.concat([df_out_aux, df_out], sort = True)
        df_out.loc[df_out['Player']== player , col] = f['counts']
    # goalkeeper
    df_gk = df_act.groupby(['Partido','Equipo','Portero/a'])['Partido','Equipo','Portero/a'].size().reset_index(name='counts')
    for i, f in df_gk.iterrows():
        if (f['Portero/a'] != "NINGUNO"):
            if (df_out[df_out.Player == f['Portero/a']].shape[0] == 0):
                team = teams[1] if f['Equipo'] == teams[0] else teams[0]
                df_out_aux=create_row(f['Partido'],team,f['Portero/a'], "GK", columns_out)
                df_out = pd.concat([df_out_aux, df_out], sort = True)
            df_out.loc[df_out['Player']==f['Portero/a'] , col] = f['counts']

df_out = detect_scoring_actions(df[df["SC Local"].notnull()]['SC Local'], match , local_team, df_out)
df_out = detect_scoring_actions(df[df["SC Visitante"].notnull()]['SC Visitante'], match ,visit_team, df_out)


dfTurnover = df[df.Posesion.notnull()]
dfTurnover = dfTurnover[dfTurnover.Posesion.str.startswith("[Error]/[Perdida]")]
df_out = register_action(dfTurnover, "Turnover", "FP", df_out)

dfSanciones = df[df.Sanciones.notnull()]
dfSanciones = dfSanciones[dfSanciones.Sanciones.str.startswith('[Exclusion]')]
df_out = register_action(dfSanciones, "2mJ", "FP", df_out)

# POST - PROCESSING : sort, infer dtypes, fillna, reset_index
df_out.sort_values(["Team", "Role", "Player"], inplace = True)
df_out = df_out.infer_objects()
df_out = df_out.fillna(0) # problema con los 7mGoal
df_out = df_out.reset_index()

# SCORING
weights = pd.Series(w, index=columns_out[6:])
weights_gk= pd.Series(w_gk, index=columns_out[6:])
df_out['Score'][df_out.Role == "FP"] = (df_out[columns_out[5:]][df_out.Role == "FP"] * weights).sum(1)
df_out['Score'][df_out.Role == "GK"] = (df_out[columns_out[5:]][df_out.Role == "GK"] * weights_gk).sum(1)
df_out['Score5'] = ((df_out['Score'] * 5) / df_out['Score'].max()).apply(truncate)
df_out['Score'] = df_out['Score'].apply(truncate)

df_out.to_excel(data_path + file_name + "_scoring.xls", columns = columns_out)
