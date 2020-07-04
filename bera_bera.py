# -*- coding: utf-8 -*-
"""
Created on Sat Jun 20 19:52:31 2020

@author: FranciscoP.Romero
"""

##
# DICCIONARIOS
##
columns_id = ["Match", "Team", "Player", "Role"]
columns_score = ["Score", "Score5", "ScorePos", "ScoreNeg", "ScoreAttack", "ScoreDef"] 
columns_kpi =  ["9mGoal",   "9mSave", "9mOut", "9mBlock",
               "6mGoal", "6mSave", "6mOut",
               "FBGoal" ,  "FBSave", "FBOut",
               "7mGoal", "7mSave", "7mOut",
               "Assist", "Received7m", "Provoke2m", "Steal","GoodDef", "Block",
               "Turnover", "DefMistake",  "2mJ", "2mBB", "RedBlueCard"
               ]
columns_out = columns_id + columns_score + columns_kpi
              

w = [1.5, -0.75, -1, -1,
           1, -0.7, -0.8,
           1, -1.5, -1.5, 
           1, -1.3, -1.3,
           0.5, 1, 0.8, 1, 0.8, 0.8,
           -0.8, -0.8, -0.8, -2, -2
           ]

cols_pos = ["9mGoal", "6mGoal", "FBGoal", "7mGoal", "Assist", "Received7m", "Provoke2m", "Steal","GoodDef", "Block"]
w_pos = [1.5, 1, 1, 1, 0.5, 1, 0.8, 1, 0.8, 0.8]
cols_neg = ["9mSave", "9mOut", "9mBlock", "6mSave", "6mOut", "FBSave", "FBOut",
            "7mSave", "7mOut", "Turnover", "DefMistake",  "2mJ", "2mBB", "RedBlueCard"]
w_neg = [-0.75, -1, -1, -0.7, -0.8, -1.5, -1.5, -1.3, -1.3, -0.8, -0.8, -0.8, -2, -2]
cols_attack = ["9mGoal",   "9mSave", "9mOut", "9mBlock",
               "6mGoal", "6mSave", "6mOut",
               "FBGoal" ,  "FBSave", "FBOut",
               "7mGoal", "7mSave", "7mOut",
               "Assist", "Received7m", "Provoke2m",  "Turnover"]
w_attack = [1.5, -0.75, -1, -1,
           1, -0.7, -0.8,
           1, -1.5, -1.5, 
           1, -1.3, -1.3,
           0.5, 1, 0.8, -0.8]
cols_def = ["Steal", "GoodDef", "Block", "DefMistake", "2mJ", "2mBB", "RedBlueCard"]
w_def = [1, 0.8, 0.8, -0.8, -0.8, -2, -2]


'''
columns_kpi =  ["9mGoal",   "9mSave", "9mOut", "9mBlock",
               "6mGoal", "6mSave", "6mOut",
               "FBGoal" ,  "FBSave", "FBOut",
               "7mGoal", "7mSave", "7mOut",
               "Assist", "Received7m", "Provoke2m", "Steal","GoodDef", "Block",
               "Turnover", "DefMistake",  "2mJ", "2mBB", "RedBlueCard"
               ]
'''
w_gk = [-1, 1, 0.5, 0.0,
           -0.6, 1.5, 0.5,
           -0.5, 1.5, 0.0, 
           -0.4, 1.5, 0.0,
           0.85, 1, 0.8, 1, 0, 0,
           -0.8, -0.8, -0.8, -2, -2
           ]

#cols_gk_pos =  ["9mSave", "9mOut", "9mBlock", "6mSave", "6mOut", "FBSave", "FBOut",
#            "7mSave", "7mOut","Assist", "Received7m", "Provoke2m", "Steal"]
cols_gk_pos =  ["9mSave", "9mOut" , "6mSave",  "6mOut","FBSave","7mSave","Assist", "Received7m", "Provoke2m", "Steal"]
cols_gk_neg = ["9mGoal", "6mGoal", "FBGoal", "7mGoal","Turnover", "DefMistake",  "2mJ", "2mBB", "RedBlueCard"]



dict_acc = {"Asistencia":"Assist", "Buena Defensa": "GoodDef", 
            "Error Defensa": "DefMistake", "Provoca 2'": "Provoke2m",
            "Blocaje": "Block", "Recuperacion": "Steal", "Recibe 7m": "Received7m"}

import pandas as pd
weights_gk_pos= pd.Series(list( filter(lambda w_gk: w_gk > 0, w_gk) ), index=cols_gk_pos)
weights_gk_neg= pd.Series(list( filter(lambda w_gk: w_gk < 0, w_gk) ), index=cols_gk_neg)


