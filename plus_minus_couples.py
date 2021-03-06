# -*- coding: utf-8 -*-
"""
Created on Thu May 14 14:13:42 2020

@author: FranciscoP.Romero
"""
import pandas as pd 
import math
data_path = "C:/Users/FranciscoP.Romero/Onedrive - Universidad de Castilla-La Mancha/RESEARCH/2005_BERABERA/datos/"
file_name = "BeraBera-Elche"
df = pd.read_csv(data_path + file_name + ".csv", sep="\t")

team = "BERA BERA"
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
plusminus_att = "Plus Minus Local" if (local_team == team) else "Plus Minus Visitante" 
oth_team = teams[0] if (teams[0] != team) else teams[1]

# filtrar posesiones
df_pm = df[["Equipo","Posesion", "Periodo", plusminus_att]][df.Posesion.notnull()]


# calculos generales
df_b = df_pm[df_pm.Equipo == team]
df_e = df_pm[df_pm.Equipo == oth_team]
pos_attack = df_b.shape[0]
goles_marc = df_b[df_b.Posesion =='[Acierto]/[Gol]'].shape[0]
pos_def = df_e.shape[0]
goles_enc = df_e[df_e.Posesion =='[Acierto]/[Gol]'].shape[0]

eff_attack  = goles_marc / pos_attack
eff_def    = 1 - (goles_enc / pos_def)

print(pos_attack, goles_marc, pos_def, goles_enc)


columns_kpi = ["Attack", "AttackPos", "AttackPlusMinus", "AttackRatio", "Def", "DefPos", "DefPlusMinus", "DefRatio"]
columns_out = ["Player1", "Player2"] + columns_kpi
df_pm_out = pd.DataFrame(columns = columns_out )

c1 = pd.Series(["05-M. PIZZO",  "06-N. TERÉS", 0,0,0,0,0,0,0,0], index = df_pm_out.columns)
c2 = pd.Series(["05-M. PIZZO",  "18-E.CESAREO", 0,0,0,0,0,0,0,0], index = df_pm_out.columns)
c3 = pd.Series(["06-N. TERÉS",  "18-E.CESAREO", 0,0,0,0,0,0,0,0], index = df_pm_out.columns)

df_pm_out = df_pm_out.append(c1, ignore_index=True)
df_pm_out = df_pm_out.append(c2, ignore_index=True)
df_pm_out = df_pm_out.append(c3, ignore_index=True)

res = 0
col = ""
for i, fila in df_pm.iterrows():
    # Compute score
    res = 0
    col = ""
    posesion = fila["Posesion"]
    if (fila["Equipo"] == team) :
        if (posesion.find ("Error") != -1):
            res = 0
        elif (posesion.find("Acierto") != -1):    
            res = 1
        col = "Attack"
        # review players
        lst_players = fila[plusminus_att].split(",")
        lst_players = [item.strip() for item in lst_players]
        for j, couple in df_pm_out.iterrows():
            if (couple["Player1"] in lst_players and couple["Player2"] in lst_players ):
                couple[col] += res
                couple[col+"Pos"] += 1
                print(couple, lst_players) 
    else: 
        if (posesion.find ("Error") != -1):
            res = 1
        elif (posesion.find("Acierto") != -1):    
            res = 0
        col = "Def"
        lst_players = fila[plusminus_att].split(",")
        lst_players = [item.strip() for item in lst_players]
        for j, couple in df_pm_out.iterrows():
            if (couple["Player1"] in lst_players and couple["Player2"] in lst_players ):
                couple[col] += res
                couple[col+"Pos"] += 1
                print(couple, lst_players)      
    
'''    
    if (posesion.find ("Error") != -1):
        res = -1 if (fila["Equipo"] == team) else 1
    if (posesion.find("Acierto") != -1):
        res = 1 if (fila["Equipo"] == team ) else -1
'''   


df_pm_out = df_pm_out.apply(pd.to_numeric, errors='ignore')

df_pm_out["AttackPlusMinus"] = ((df_pm_out["Attack"]/ df_pm_out["AttackPos"]) - eff_attack)*100
df_pm_out["DefPlusMinus"] = ((df_pm_out["Def"]/ df_pm_out["DefPos"]) - eff_def)*100
df_pm_out["AttackRatio"] = (df_pm_out["AttackPos"] / pos_attack) * 100
df_pm_out["DefRatio"] = (df_pm_out["DefPos"] / pos_def) * 100

df_pm_out.fillna(0, inplace=True)
df_pm_out[columns_kpi] = df_pm_out[columns_kpi].round()

df_pm_out.to_excel(data_path + file_name + "_plusminus_parejas.xls", columns = columns_out)

#df_pm_out.plot(x = "Player", y = "AttackPlusMinus", kind='bar')
#df_pm_out.plot(x = "Player", y = "DefPlusMinus", kind='bar')    
    
    