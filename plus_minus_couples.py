# -*- coding: utf-8 -*-
"""
Created on Fri May 15 08:42:52 2020

@author: FranciscoP.Romero
"""

import pandas as pd 
data_path = "C:/Users/FranciscoP.Romero/Onedrive - Universidad de Castilla-La Mancha/RESEARCH/2005_BERABERA/"
file_name = "BeraBera-Gijon"
df = pd.read_csv(data_path + file_name + ".csv", sep="\t")
team = "BERA BERA"
plusminus_att = "Plus Minus Local"

df_pm = df[["Equipo","Posesion", plusminus_att]][df.Posesion.notnull()]
columns = ["Player1", "Player2","PlusMinus", "Appareances"]
df_pm_out = pd.DataFrame(columns=columns )

c1 = pd.Series(["05-M. PIZZO",  "06-N. TERÉS", 0, 0], index = df_pm_out.columns)
c2 = pd.Series(["05-M. PIZZO",  "18-E.CESAREO", 0, 0], index = df_pm_out.columns)
c3 = pd.Series(["06-N. TERÉS",  "18-E.CESAREO", 0, 0], index = df_pm_out.columns)

df_pm_out = df_pm_out.append(c1, ignore_index=True)
df_pm_out = df_pm_out.append(c2, ignore_index=True)
df_pm_out = df_pm_out.append(c3, ignore_index=True)



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
    lst_players = [item.strip() for item in lst_players]
    for j, couple in df_pm_out.iterrows():
        if (couple["Player1"] in lst_players and couple["Player2"] in lst_players ):
            couple["PlusMinus"] += res
            couple["Appareances"] += 1
            print(couple, lst_players)
    
    
df_pm_out.to_excel(data_path + file_name + "_plusminus_parejas.xls", columns = columns)


