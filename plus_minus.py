# -*- coding: utf-8 -*-
"""
Created on Thu May 14 14:13:42 2020

@author: FranciscoP.Romero
"""
import pandas as pd 
data_path = "C:/Users/FranciscoP.Romero/Onedrive - Universidad de Castilla-La Mancha/RESEARCH/2005_BERABERA/datos/"
file_name = "Berabera-Elche"
df = pd.read_csv(data_path + file_name + ".csv", sep="\t")
team = "BERA BERA"
plusminus_att = "Plus Minus Local"

df_pm = df[["Equipo","Posesion", plusminus_att]][df.Posesion.notnull()]

df_b = df_pm[df_pm.Equipo == "BERA BERA"]
df_e = df_pm[df_pm.Equipo == "ELCHE"]
pos_attack = df_b.shape[0]
goles_marc = df_b[df_b.Posesion =='[Acierto]/[Gol]'].shape[0]
pos_def = df_e.shape[0]
goles_enc = df_e[df_e.Posesion =='[Acierto]/[Gol]'].shape[0]

eff_attack  = goles_marc / pos_attack
eff_deff    = 1 - (goles_enc / pos_def)



df_pm_out = pd.DataFrame(columns= ["Match", "Player","PMB", "Appareances"])

res = 0
for i, fila in df_pm.iterrows():
    # Compute score
    res = 0
    posesion = fila["Posesion"]
    if (posesion.find ("Error") != -1):
        res = -1 if (fila["Equipo"] == team) else 1
    if (posesion.find("Acierto") != -1):
        res = 1 if (fila["Equipo"] == team ) else -1
    # review players
    lst_players = fila[plusminus_att].split(",")
    for player in lst_players:
        player = player.strip()
        if (df_pm_out[df_pm_out.Player == player].shape[0] == 0):
            df_player = pd.DataFrame([[player,0,0]], columns=["Player","PMB", "Appareances"] )
            df_pm_out = pd.concat([df_player, df_pm_out])
        df_pm_out.loc[df_pm_out['Player']== player , "PlusMinus"] += res
        df_pm_out.loc[df_pm_out['Player']== player , "Appareances"] += 1


df_pm_out.to_excel(data_path + file_name + "_plusminus.xls", columns = ["Player","PMB", "Appareances"])

df_pm_out.plot(x = "Player", y = "PlusMinus", kind='bar')
    
    
    