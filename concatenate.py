# -*- coding: utf-8 -*-
"""
Created on Tue Jun 25 08:47:41 2019

@author: sumedh
"""
import glob
import os
import pandas as pd
import logging
# specific loggers
logger = logging.getLogger(__name__)
formatter = logging.Formatter('%(asctime)s: %(levelname)s: %(name)s: %(message)s')
file_handler = logging.FileHandler('concatenate.log')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.DEBUG)
path = 'D:/Github/JobScrapper-v2/'
list_of_files = glob.glob(path+'daily_data/*')
latest_file = max(list_of_files, key=os.path.getctime)
print (latest_file)
directory = path+'master_data/master.csv'

if not os.path.exists(directory):
    with open(directory, "w") as p:
        pass
else:
    try:
        df1 = pd.read_csv(directory)
        logger.debug('df1 has {} rows and {} columns'.format(len(df1),len(df1.columns)))
        df2 = pd.read_csv(latest_file)
        logger.debug('df2 has {} rows and {} columns'.format(len(df2),len(df2.columns)))
        df = df1.append(df2)
        logger.debug('df has {} rows and {} columns'.format(len(df),len(df.columns)))
    except Exception:
        logger.warn('No file detcted, creating new file', exc_info = True)
        df = pd.read_csv(latest_file)

df = df.drop_duplicates('Job_Id')
logger.info('Duplicates dropped, proceeding to save to file')
df.to_csv(directory, index = False)
