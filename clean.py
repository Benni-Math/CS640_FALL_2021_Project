import json

import pandas as pd
import numpy as np
from pandas import merge

print(pd.__version__)

# Data reading

user_demo = pd.read_json("User demo profiles.json", encoding="utf-8", orient='records')
label = pd.read_csv("labeled_users.csv")

# Data cleaning
# regexMap = {r"<[\w'/'\s]*>": "", r"[\"\-]+": "", r"@[\w]+": "", r"<(\S*?)[^>]*>.*?|<.*? />": "",
#             r"[a-zA-z]+://[^\s]*": ""}
#
#
# def preprocess(datainput):
#     t = datainput
#     for regx in regexMap.keys():
#         t = re.sub(regx, regexMap[regx], t)
#     return t


# join two tables by id
clean = pd.merge(label, user_demo, how='inner', left_on="user_id", right_on="id")
clean = clean[['user_id', 'year_born', 'race', 'img_path']]

# remove nan and digital number
clean = clean.dropna(axis=0,how='any')
clean.isnull().any()
clean['year_born'] = clean['year_born'].astype(int)
clean['race'] = clean['race'].astype(int)
clean['user_id'] = clean['user_id'].astype(int)

# add a column about age
clean['age'] = 2021 - clean['year_born']
clean['over21'] = 1
clean['over21'][clean['age'] < 21] = 0     # clean.over21[clean.age < 21] = 0

# remove Multiracial race (5)
clean = clean.drop(index = (clean.loc[(clean['race']==5)].index))

# write clean dataset
# clean.to_csv('clean.csv', encoding='utf-8', index = None)