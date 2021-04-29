# -*- coding: utf-8 -*-
"""
Created on Tue Dec  4 12:35:05 2018
Project: Entity Extraction from Statements (Al Marai)
@author: Deepak.Reji
"""
# Importing package for reading table
from tabula import read_pdf

# Read the Statement and load it as a dataframe
import os
os.chdir('F:\\Files\\Statements')

Statement = read_pdf('Al Marai.pdf')

# Replacing none values with a string to perform search
Statement = Statement.fillna("(no values)")

# Extracting Customer Number
Customer_No = Statement[Statement.iloc[:, 0].str.contains("Customer No")].iloc[:,0].str.split(':').str[1].iloc[0]

# Extracting Customer Name
Name = Statement[Statement.iloc[:, 0].str.contains("Name")].iloc[:,0].str.split(':').str[1].iloc[0]

# Extracting Credit days
Credit_days = Statement[Statement.iloc[:, 0].str.contains("Credit Days")].iloc[:,0].str.split(':').str[1].iloc[0]

# Extracting Statement date
Statement_date = Statement[Statement.iloc[:, 3].str.contains("Statement Date")].iloc[:, 4].iloc[0]

# Extracting Transaction Range
Transaction_Range = Statement[Statement.iloc[:, 3].str.contains("Transaction Range")].iloc[:, 4].iloc[0]

# Extracting Payment Due Date
Payment_Due_Date = Statement[Statement.iloc[:, 3].str.contains("Payment Due Date")].iloc[:, 4].iloc[0]

# Extracting Currency
Currency =  Statement[Statement.iloc[:, 8].str.contains("Figures in")].iloc[:, 8].str.split(':').str[1].iloc[0]

# Creating a Dataframe with default key objects
Key = ["Customer No", "Name", "Credit Days", "Statement Date", "Transaction Range", "Payment Due Date", "Currency"]

import pandas as pd
Entity = pd.DataFrame(data = [Customer_No, Name, Credit_days, Statement_date, Transaction_Range,Payment_Due_Date, Currency], index = Key)

# Remove (:) symbol from a column 
Entity[0] = Entity[0].str.replace(':', '')

# Remove trailing white spaces in the column
Entity[0] = Entity[0].str.strip()

# Output-1
# Writing file into a directory
Entity 
Entity.to_csv("F:\Files\Statements\Entity.csv", encoding='utf-8')



# Searching for the index which helps in extracting the table
a = Statement[Statement.iloc[:, 2].str.contains("no values")].iloc[:, 2:9].index[0]
b =  Statement[Statement.iloc[:, 2].str.contains("no values")].iloc[:, 2:9].index[2]

# Subsetting the dataframe
df = Statement.iloc[a+1:b, 2:9]

# Dropping columns
df = df.drop(columns = ['Unnamed: 6'])

# Re-naming the rows 
df.columns = df.iloc[0]
df = df.reindex(df.index.drop(1))

# Resetting the index
df = df.reset_index(drop=True)

# Adding a identifier with the dataframe
df.insert(0, 'Customer Number', Customer_No)

# Output-2
# Writing file into a directory
df.to_csv("F:\Files\Statements\df.csv", encoding='utf-8', index=False)
