# -*- coding: utf-8 -*-
"""
scoring total
Calculo de
"""
from handball_functions import * # functions
from bera_bera import * # dictionaries
import pandas as pd


# 0. load data
data_path = "C:/Users/FranciscoP.Romero/Desktop/BERA BERA 20-21/datos/"
file_name = "200812_BER-ZUA"
df = pd.read_csv(data_path + file_name + ".csv", sep="\t")


matches = df["Partido"].unique()
main_team = "BERA BERA"
# prepare ouput
df_xls = pd.DataFrame(columns= columns_out)

for match in matches: 
    df_match = df[df["Partido"] == match]
    teams = df_match["Equipo"].unique()
    df_out = pd.DataFrame(columns= columns_out)
    local_team, visit_team = local_visitante(teams, match, main_team)
    #Goals
    dfGoal= df_match[['Partido','Equipo', 'Jugador/a', 'Zona Accion', 'Portero/a']][df_match.Posesion=="[Acierto]/[Gol]"]
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
    dfSave = df_match[df_match.Posesion == "[Error]/[Parada]"]
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
    dfOut = df_match[df_match.Posesion == "[Error]/[Fuera]"]
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
    
    df_pos = df_match[df_match.Posesion == "[Error]/[Blocaje]"]
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
    
    
    df_out = detect_scoring_actions(df_match[df_match["SC Local"].notnull()]['SC Local'], match , local_team, df_out, dict_acc, columns_out)
    df_out = detect_scoring_actions(df_match[df_match["SC Visitante"].notnull()]['SC Visitante'], match ,visit_team, df_out, dict_acc, columns_out)
    
    
    dfTurnover = df_match[df.Posesion.notnull()]
    dfTurnover = dfTurnover[dfTurnover.Posesion.str.startswith("[Error]/[Perdida]")]
    df_out = register_action(dfTurnover, "Turnover", "FP", df_out, columns_out)
    
    dfSanciones = df_match[df.Sanciones.notnull()]
    dfSanciones = dfSanciones[dfSanciones.Sanciones.str.startswith('[Exclusion]')]
    df_out = register_action(dfSanciones, "2mJ", "FP", df_out, columns_out)
    
    # SCORING
    
    weights = pd.Series(w, index=columns_kpi)
    weights_pos = pd.Series(w_pos, index = cols_pos)
    weights_neg = pd.Series(w_neg, index = cols_neg)
    
    weights_gk= pd.Series(w_gk, index=columns_kpi)
    
    df_out['Score'][df_out.Role == "FP"] = (df_out[columns_kpi][df_out.Role == "FP"] * weights).sum(1)
    df_out['Score'][df_out.Role == "GK"] = (df_out[columns_kpi][df_out.Role == "GK"] * weights_gk).sum(1)
    df_out['Score5'] = ((df_out['Score'] * 5) / df_out['Score'].max()).apply(truncate)
    
    
    df_out['ScorePos'][df_out.Role == "FP"] = (df_out[cols_pos][df_out.Role == "FP"] * weights_pos).sum(1)
    df_out['ScorePos'][df_out.Role == "GK"] = (df_out[cols_gk_pos][df_out.Role == "GK"] * weights_gk_pos).sum(1)
    
    df_out['ScoreNeg'][df_out.Role == "FP"] = (df_out[cols_neg][df_out.Role == "FP"] * weights_neg).sum(1)
    df_out['ScoreNeg'][df_out.Role == "GK"] = (df_out[cols_gk_neg][df_out.Role == "GK"] * weights_gk_neg).sum(1)
    
    weights_attack = pd.Series(w_attack, index = cols_attack)
    weights_def = pd.Series(w_def, index = cols_def)
    df_out['ScoreAttack'][df_out.Role == "FP"] = (df_out[cols_attack][df_out.Role == "FP"] * weights_attack).sum(1)
    df_out['ScoreDef'][df_out.Role == "FP"] = (df_out[cols_def][df_out.Role == "FP"] * weights_def).sum(1)
    
    
    # truncate TODO reducir
    df_out['Score'] = df_out['Score'].apply(truncate)
    df_out['ScorePos'] = df_out['ScorePos'].apply(truncate)
    df_out['ScoreNeg'] = df_out['ScoreNeg'].apply(truncate)
    df_out['ScoreAttack'] = df_out['ScoreAttack'].apply(truncate)
    df_out['ScoreDef'] = df_out['ScoreDef'].apply(truncate)

    df_xls = df_xls.append(df_out)

df_xls[columns_out].to_excel(data_path + "1920_scoring.xls", columns = columns_out)

bera_bera = df_xls[df_xls["Team"] == "BERA BERA"]
bera_bera[["Player", "Score5"]].groupby("Player").sum()

columns = ["Player", "Role"] + list(matches)
df_pvt = pd.pivot_table(bera_bera, values = 'Score', index=['Player', 'Role'], columns = 'Match').reset_index()
df_pvt.fillna(0, inplace=True)
#df_pvt = df_pvt[df_pvt.Role == "FP"][columns]
df_pvt = df_pvt[columns]
df_pvt.to_excel(data_path + "1920_table.xls")

