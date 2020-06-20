# -*- coding: utf-8 -*-
"""
Created on Sat Jun 20 19:41:15 2020

@author: FranciscoP.Romero
"""
import pandas as pd
import math

def local_visitante(teams, match,team): 
    # local y visitante
    pos_guion = match.find("-")
    pos_team = match.find(team)
    oth_team = teams[0] if (teams[0] != team) else teams[1]
    local_team = team if pos_guion > pos_team else oth_team
    visit_team = oth_team if pos_guion > pos_team else team
    return local_team, visit_team


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


def detect_scoring_actions(actions, match, team, df_out, dict_acc, columns_out):
    for act in actions:
        # control multiple action to a single player
        num_players = act.count(":")
        num_actions = act.count(",")
        if (num_players == 1 and  num_actions > 0): 
            player = act[: act.find(":")].strip()
            pos_comma = act.find(",")
            act = act[:pos_comma + 1] + player + ":" + act[pos_comma + 1: ]
        ## processing
        a_lst = act.split(",")
        for a in a_lst:
            pos = a.find(":")
            player =  a[: pos].strip()
            accion = a[pos + 1: ].strip()
            ## borrar etiquetado ocasional
            accion = accion.strip("[")
            accion = accion.strip("]")
            col = dict_acc.get(accion)
            if (col is not None):
                if (df_out[df_out.Player == player].shape[0] == 0):
                    df_out_aux=create_row(match,team, player, "FP", columns_out)
                    df_out = pd.concat([df_out_aux, df_out], sort = True)
                # contar jugada
                df_out.loc[df_out['Player']== player, col] +=1
    return df_out



def register_action(df, col, role, df_out, columns_out):
    for i, f in df.iterrows():
        player = f['Jugador/a'].strip()
        if (df_out[df_out.Player == player].shape[0] == 0):
            df_out_aux=create_row(f['Partido'],f['Equipo'],player, role, columns_out)
            df_out = pd.concat([df_out_aux, df_out], sort = True)
        df_out.loc[df_out['Player'] == player , col] += 1
    return df_out