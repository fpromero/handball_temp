# -*- coding: utf-8 -*-
"""
Created on Fri May  8 10:05:36 2020

@author: FranciscoP.Romero
"""


## DOWNLOAD EURO 2020    
    
ehf2020_path = 'https://livecache.sportresult.com/node/binaryData/HBL_PROD/HBEC20M/PDF_PXXTM.PDF'

for i in range (1, 66): 
    match_index = (str(i) if (i >= 10) else ('0' + str(i)) )
    url = ehf2020_path.replace('XX', match_index)
    myfile = requests.get(url)
    open('C:/Users/FranciscoP.Romero/Desktop/euro2020/' + match_index + '.pdf', 'wb').write(myfile.content)
    