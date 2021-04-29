# -*- coding: utf-8 -*-
"""
Created on Wed Dec 19 21:07:42 2018

Project: Entity Recognition from Bills
@author: Deepak.Reji
"""
# Reading the File
import os
os.chdir('F:\\Files\\Bill Documents')

# Reading the text file and storing it as string
with open("page1.txt", 'r') as myfile:
    text=myfile.read().replace('\n', '\n')

# Installing nltk and its dependencies
import nltk
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag

# Extraction function to extract all the informations
def extract_Basic(sent):
    grammar = r"""
    NBAR:
        {<NNP><NNP.*>?<CD*>}
    NP:
        {<NBAR>}
        # Above, connected with in/of/etc...
        {<NBAR><IN><NBAR>}
    """
    chunker = nltk.RegexpParser(grammar)
    ne = set()
    chunk = chunker.parse(nltk.pos_tag(nltk.word_tokenize(sent)))
    for tree in chunk.subtrees(filter=lambda t: t.label() == 'NP'):
        ne.add(' '.join([child[0] for child in tree.leaves()]))
    return ne

Basic = []
Basic+= extract_Basic(text)

# Converting the list into a Dataframe
import pandas as pd
df1 = pd.DataFrame(Basic)

# Importing json file and converting it into a dataframe
import json
with open('bill_dict.json', 'r') as fp:
    attributes = json.load(fp)
data = pd.DataFrame.from_dict(attributes, orient='columns')

# Selecting unique values and storing in a dataframe
labels = data['label'].unique()
df = pd.DataFrame(labels)
df.columns = ["label"]
    
# Searching the element and storing in a list
import sys
a = []
for j in data['text']:
    try:
        a+= [df1[df1[0].str.contains(j)].iloc[0].str.split().str[2].iloc[0]]        
    except:
        a+= ["None"]
        print("No Searched Results")

# Data Manipulation
data['value'] = a        
data = data.drop(['text'], axis = 1)        
data =data[data.value != 'None']
data = data.drop_duplicates(keep='last') 

# Merging the values into main dataframe
df = pd.merge(df, data, on = "label", how = "inner")

# Final cleaning
df.index = df['label']
df = df.drop(['label'], axis =1)

# Converting dataframe to json file    
df.to_json(orient='index')

# Writing files to a storage location
df.to_csv("F:\Files\Bill Documents\dataframe.csv", encoding='utf-8', index=True)



