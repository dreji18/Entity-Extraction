# -*- coding: utf-8 -*-
"""
Created on Wed Nov 28 14:34:25 2018

Task: Entity Recognition using NLTK
@author: Deepak.Reji
"""

# Setting the working directory
import os
os.chdir('F:\\Files\\tickets')

# Reading the text file and storing it as string
with open("text6legs.txt", 'r') as myfile:
    text=myfile.read().replace('\n', '')

# Splitting the whole string based on different Legs  
d = "Leg"
s=text.split(d)
split=list()
split.append(s[0])
split+=[d + s for s in s[1:]]

# Installing nltk and its dependencies
import nltk
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag

# Extracting Entity from a Sentence using POS tagging and Chunking
# Returns Entities such as Date,Check-in time, Departure time, Arrival time, Flight number, Leg(Optional), Terminal  
def extract_Basic(sent):
    grammar = r"""
    NBAR:
        {<NNP.*>?<CD*>}
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

# Looping across the splitted strings
Basic = []
for i in range(len(split)):
    sample = []
    sample+= extract_Basic(split[i])
    Basic.append(sample)
    
# Returns Seat Status
def extract_Additional(sent):
    grammar = r"""
    NBAR:
        #
        {<NNP> <NNP> <NNP>}
    NP:
        {<NBAR>}
        # Above, connected with in/of/etc...
        {<NBAR><TO><NBAR>}
    """
    chunker = nltk.RegexpParser(grammar)
    ne = set()
    chunk = chunker.parse(nltk.pos_tag(nltk.word_tokenize(sent)))
    for tree in chunk.subtrees(filter=lambda t: t.label() == 'NP'):
        ne.add(' '.join([child[0] for child in tree.leaves()]))
    return ne

# Looping across the splitted strings
Additional = []
for i in range(len(split)):
    sample1 = []
    sample1+= extract_Additional(split[i])
    Additional.append(sample1)
    
# Returns Arrival and Departure
def extract_Location(sent):
    grammar = r"""
    NBAR:
        #
        {<NNP*>?<NNP*><,><NNP>}
    NP:
        {<NBAR>}
        # Above, connected with in/of/etc...
        {<NBAR><NBAR>}
    """
    chunker = nltk.RegexpParser(grammar)
    ne = set()
    chunk = chunker.parse(nltk.pos_tag(nltk.word_tokenize(sent)))
    for tree in chunk.subtrees(filter=lambda t: t.label() == 'NP'):
        ne.add(' '.join([child[0] for child in tree.leaves()]))
    return ne   

# Looping across the splitted strings
Location = []
for i in range(len(split)):
    sample2 = []
    sample2+= extract_Location(split[i])
    Location.append(sample2)

# Converting the Lists of Lists to a dataframe
import pandas as pd
df1 = pd.DataFrame(Basic)
df1 = df1.T
df2 = pd.DataFrame(Additional)
df2 = df2.T
df3 = pd.DataFrame(Location)
df3 = df3.T

# Removing the first row
df1.drop(df1.columns[[0]], axis=1, inplace=True)
df2.drop(df2.columns[[0]], axis=1, inplace=True)
df3.drop(df3.columns[[0]], axis=1, inplace=True)

# Concatenating both the dataframes
df = pd.concat([df1, df2, df3])

# Replacing none values with a string to perform search
df = df.fillna("(no values)")

# Resetting the index
df = df.reset_index(drop=True)
    
# Creating a list to collect all the Flight number
Flight=[]
for k in range(1, len(df.columns)+1):
    Flight+=  [df[df[k].str.contains("EK")][k].iloc[0]]
    
# Creating a list to collect all the Leg number
Leg=[]
for k in range(1, len(df.columns)+1):
    Leg+=  [df[df[k].str.contains("Leg")][k].iloc[0]]
    
# Creating a list to collect all the Check-in time   
Check_in=[]
for k in range(1, len(df.columns)+1):
    Check_in+=  [df[df[k].str.contains("Opens")][k].str.split().str[1].iloc[0]]   

# Creating a list to collect all the Departure time   
Departure=[]
for k in range(1, len(df.columns)+1):
    Departure+=  [df[df[k].str.contains("Departure")][k].str.split().str[1].iloc[0]]  

# Creating a list to collect all the Arrival time   
Arrival=[]
for k in range(1, len(df.columns)+1):
    Arrival+=  [df[df[k].str.contains("Arrival")][k].str.split().str[1].iloc[0]]  
    
# Creating a list to collect all the Seat Status  
Status=[]
for k in range(1, len(df.columns)+1):
    Status+=  [df[df[k].str.contains("Seat Status")][k].str.split().str[2].iloc[0]]  

# Creating a list to collect all the Source locations  
Source=[]
for k in range(1, len(df.columns)+1):
    Source+=  [df[df[k].str.contains("Departing")][k].str.split().str[3].iloc[0]]  

# Creating a list to collect all the Source locations  
Destination=[]
for k in range(1, len(df.columns)+1):
    Destination+=  [df[df[k].str.contains("Arriving")][k].str.split().str[3].iloc[0]]   
    
# Creating a list to collect all the Terminal number 
Terminal=[]
for k in range(1, len(df.columns)+1):
    Terminal+=  [df[df[k].str.contains("Terminal")][k].str.split().str[1].iloc[0]]
    
# Extracting Journey dates
import re
Dates = []
for i in range(1, len(df.columns)+1):
    for j in range(len(df)):
        Dates+= re.findall(r"[\d]{1,2}[ADFJMNOS]\w*[\d]{4}", df[i][j])
      
# Final dataframe for storing Entities
Entity_df = pd.DataFrame(data = [Flight, Leg, Dates, Check_in, Departure, Arrival, Status, Source, Destination, Terminal])   

# Indexing the Dataframe
Entity_df.index = ['Flight No', 'Leg', 'Journey Date', 'Check_in', 'Departure', 'Arrival', 'Status', 'Source', 'Destination', 'Terminal']

# Re-naming the columns
Entity_df.columns = range(1, len(Entity_df.columns)+1)

# Transposing and finalising the dataframe
Entity_df = Entity_df.T



