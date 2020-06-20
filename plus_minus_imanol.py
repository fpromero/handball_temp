# -*- coding: utf-8 -*-
"""
Created on Thu May 14 14:13:42 2020

@author: FranciscoP.Romero
"""

def local_visitante(teams, match,team): 
    # local y visitante
    pos_guion = match.find("-")
    pos_team = match.find(team)
    oth_team = teams[0] if (teams[0] != team) else teams[1]
    local_team = team if pos_guion > pos_team else oth_team
    visit_team = oth_team if pos_guion > pos_team else team
    return local_team, visit_team

import pandas as pd 



team = "BERA BERA"
columns_kpi = ["Attack", "AttackPos", "AttackPlusMinus", "AttackRatio", "Def", "DefPos", "DefPlusMinus", "DefRatio"]
columns_out = ["Match", "Player"] + columns_kpi
df_out = pd.DataFrame(columns = columns_out )

''' opcion fichero con multipartido '''
data_path = "C:/Users/FranciscoP.Romero/Desktop/"
file_name = "1920_BERABERA_FULL"
df_full = pd.read_csv(data_path + file_name + ".csv", sep="\t")

matches = df_full["Partido"].unique()
df_matches = []

for match in matches: 
    df = df_full[df_full["Partido"] == match]
    df_pm_out = pd.DataFrame(columns = columns_out )
    # match features
    teams = df["Equipo"].unique()
    match = df["Partido"].unique()[0]
    local_team, visit_team = local_visitante(teams, match, team)
    plusminus_att = "Plus Minus Local" if (local_team == team) else "Plus Minus Visitante" 
    oth_team = teams[0] if (teams[0] != team) else teams[1]
    # filtrar posesiones
    df_pm = df[["Equipo","Posesion", "No Posesion", "Periodo", plusminus_att]][df.Posesion.notnull()]
    df_pm = df_pm[df["No Posesion"] == False]
    df_pm = df_pm[df_pm[plusminus_att].notnull()]

    # calculos generales
    df_b = df_pm[df_pm.Equipo == team]
    df_e = df_pm[df_pm.Equipo == oth_team]
    pos_attack = df_b.shape[0]
    goles_marc = df_b[df_b.Posesion =='[Acierto]/[Gol]'].shape[0]
    pos_def = df_e.shape[0]
    goles_enc = df_e[df_e.Posesion =='[Acierto]/[Gol]'].shape[0]
    
    eff_attack  = goles_marc / pos_attack
    eff_def    = 1 - (goles_enc / pos_def)
    
    print(match)
    print(pos_attack, goles_marc, pos_def, goles_enc)



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
            
        else: 
            if (posesion.find ("Error") != -1):
                res = 1
            elif (posesion.find("Acierto") != -1):    
                res = 0
            col = "Def"
        lst_players = fila[plusminus_att].split(",")
        for player in lst_players:
            player = player.strip()
            if (df_pm_out[(df_pm_out.Player == player)].shape[0] == 0):
                df_player = pd.DataFrame([[match, player,0,0,0,0,0,0,0,0]], columns = columns_out)
                df_pm_out = pd.concat([df_player, df_pm_out])
            df_pm_out.loc[df_pm_out['Player']== player , col] += res
            df_pm_out.loc[df_pm_out['Player']== player , col+"Pos"] += 1        
 

    df_pm_out = df_pm_out.apply(pd.to_numeric, errors='ignore')
    
    df_pm_out["AttackPlusMinus"] = ((df_pm_out["Attack"]/ df_pm_out["AttackPos"]) - eff_attack)*100
    df_pm_out["DefPlusMinus"] = ((df_pm_out["Def"]/ df_pm_out["DefPos"]) - eff_def)*100
    df_pm_out["AttackRatio"] = (df_pm_out["AttackPos"] / pos_attack) * 100
    df_pm_out["DefRatio"] = (df_pm_out["DefPos"] / pos_def) * 100
    
    df_matches.append(df_pm_out)
    
    
df_out = pd.concat(df_matches)

df_out.fillna(0, inplace=True)
df_out[columns_kpi] = df_out[columns_kpi].round()

df_out.to_excel(data_path + file_name + "_plusminus_imanol.xls", columns = columns_out)



    
    