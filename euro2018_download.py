# -*- coding: utf-8 -*-
"""
Created on Fri May  8 10:06:33 2020

@author: FranciscoP.Romero
"""


## DOWNLOAD EURO 2018
main_path = 'http://home.eurohandball.com/ehf_files/specificHBI/ECh_Analyses/2018/CRO/2/2/'
for i in range (1, 48): 
	file_name = (str(i) if (i >= 10) else ('0' + str(i)) )+ '.pdf'
	print (file_name)
	url = main_path + file_name
	myfile = requests.get(url)
	open('C:/Users/FranciscoP.Romero/Desktop/euro2018/' + file_name, 'wb').write(myfile.content)
    
    
    