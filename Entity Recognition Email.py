    # -*- coding: utf-8 -*-
"""
Created on Mon Dec  3 11:52:10 2018
Project: Entity Extraction from E-mail content
@author: Deepak.Reji
"""
# Set working directory
import os
os.chdir('F:\\Files\\Email Use Case')

# Reading the text file and storing it as string
with open("email_text.txt", 'r') as myfile:
    text=myfile.read().replace('\n', '')

# Importing Package
import PyPDF2

# Reading the file
pdfReader = PyPDF2.PdfFileReader("Initiation mail.pdf")

# No. of Pages
n=pdfReader.numPages

# Extracting the text from pages
finalText=""
for i in range(n):
    pageObj = pdfReader.getPage(i)
    text=pageObj.extractText()
    finalText=finalText+text+" "

import re
trial= re.sub('[^A-Za-z0-9]+', '', finalText)

cleanString = re.sub('\W+'," ", finalText )

# Installing nltk and its dependencies
import nltk
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag

finalText = finalText.replace(':', ',')

def extract_Basic(sentence):
    grammar = r"""
    NBAR:
        {<NNP><,><NNP>}
    NP:
        {<NBAR>}
        # Above, connected with in/of/etc...
        {<NBAR><NBAR>}
    """
    chunker = nltk.RegexpParser(grammar)
    ne = set()
    chunk = chunker.parse(nltk.pos_tag(nltk.word_tokenize(sentence)))
    for tree in chunk.subtrees(filter=lambda t: t.label() == 'NP'):
        ne.add(' '.join([child[0] for child in tree.leaves()]))
    return ne

extract_Basic(finalText)

