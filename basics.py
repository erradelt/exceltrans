import os
import pandas as pd
import re
import openpyxl
import math
from collections import defaultdict, Counter

import filepathgen as fg #module that generates filpath to the current directory
from equipment import equipment_types as et #dict containing the types of equipment

#setting path to file by using the module filepathgen, this only works, if the list is located in the same 
#directory as the program

#filepaths
excel_path: str = os.path.join(fg.current_directory, 'basisliste.xlsx') # path for loading excel
text_path: str = os.path.join(fg.current_directory, 'dataset.txt') # path for saving overview of items as .txt

df = pd.read_excel(excel_path, header=1) #header = 1 -> first row will be ignored (default: header = 0)

datacontainer: list = []
i_lst: list = [] # list thats used to save all the indices of rows without content
for index, row in df.iterrows():
    # Convert the row to a dictionary, for instance
    dataset = row.to_dict()
    if pd.isna(row['Familie']): #pd.isna is build in pandas function to check for empty cells. the line checks for an empty cell in every row of the column 'Familie'
        i_lst.append(index)
    datacontainer.append(dataset)

datacontainer_cleaned = [item for i, item in enumerate(datacontainer) if i not in i_lst] # generate new list without empty items

# find all categories in the dataset (datacontainer_cleaned)
categories_all: list = []
for data in datacontainer_cleaned:
    cat: str = str(data['Art'])
    categories_all.append(cat)

# extract the codes of each item from the dataset
categories: list = list(dict.fromkeys(categories_all)) # delete doublicates
types_raw: list = []
for art in datacontainer_cleaned:
    cat_temp: str = str(art['Art']) #temporarily extract the type of each item
    if cat_temp in categories_all: #if type matches a category add the code of the item to the list 'types_raw'
        types_raw.append(str(art['Codierung']))

# count how often a specific 'Codierung' occours and generate dict that saves these values
types: dict ={}
for item in types_raw: # create dict and count number of occurances per item
    if item in types:
        types[item] +=1
    else:
        types[item] = 1

types_sorted:dict = defaultdict(list)
for key, value in types.items():
    temp:str = str(key)
    for category in categories:
        if temp.startswith(category):  # Check if the key starts with the category
            types_sorted[category].append({key: value})
  
out_to_excel: list = []

for key, list_of_dicts in types_sorted.items():
    for item in list_of_dicts:
        for sub_key, value in item.items():
            out_to_excel.append({'Categorie':key, 'Code':sub_key, 'Menge':value})
 

of = pd.DataFrame(out_to_excel)

of.to_excel('basisliste_sorted.xlsx', index=False)

