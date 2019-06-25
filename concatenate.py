# -*- coding: utf-8 -*-
"""
Created on Tue Jun 25 08:47:41 2019

@author: sumedh
"""
import glob
import os
import pandas as pd

path = 'D:/Github/JobScrapper-v2/'
list_of_files = glob.glob(path+'daily_data/*')
latest_file = max(list_of_files, key=os.path.getctime)
print (latest_file)

directory = path+'master_data/master.csv'
if not os.path.exists(directory):
    with open(directory, "w") as p:
        pass
else:
    df1 = pd.read_csv(directory)
    
df2 = pd.read_csv(latest_file)

df = df1.append(df2)
df = df.drop_duplicates('Job_Id')
df.to_csv(directory, index = False)
