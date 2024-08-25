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

df = pd. read_excel(excel_path, header=1) #header = 1 -> first row will be ignored (default: header = 0)

datacontainer: list = []
i_lst: list = [] # list thats used to save all the indices of rows without content
for index, row in df.iterrows():
    # Convert the row to a dictionary, for instance
    dataset = row.to_dict()
    if pd.isna(row['Familie']): #pd.isna is build in pandas function to check for empty cells. the line checks for an empty cell in every row of the column 'Familie'
        i_lst.append(index)
    datacontainer.append(dataset)

datacontainer_cleaned = [item for i, item in enumerate(datacontainer) if i not in i_lst] # generate new list without empty items

categories_all: list = []
for data in datacontainer_cleaned:
    cat: str = str(data['Art'])
    categories_all.append(cat)

categories: list = list(dict.fromkeys(categories_all))
types_raw: list = []
for art in datacontainer_cleaned:
    cat_temp: str = str(art['Art'])
    if cat_temp in categories:
        types_raw.append(str(art['Codierung']))

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

for category in types_sorted:
    types_sorted[category] = sorted(types_sorted[category], key=lambda x: list(x.values())[0], reverse=True)

rooms: dict ={}

type_keys: list = []
for value in types_sorted.values():
    for i in range(len(value)):
        type_keys.append(value[i].keys())

for type in type_keys: 
    for d in datacontainer_cleaned:
        if type in d.values():
            rooms[d['MEP-Raum: Name']] = 1
        else:
            rooms[d['MEP-Raum: Name']] = rooms.get(d['MEP-Raum: Name'], 0) +1

print(rooms)
"""

for d in datacontainer_cleaned:
    for value in types_sorted.values():
        print(value)
        pass
        if value in d.values():
            rooms[d['MEP-Raum: Name']] = rooms.get(d['MEP-Raum: Name'], 0) + 1
        else:
            rooms[d['MEP-Raum: Name']] = 1

print(rooms)




with open (text_path, 'w') as file: #write textfile
    for typ_key, values in types_sorted.items(): #iterate through types
        file.write(f'{typ_key}\n') #write key in one line
        for item in values: #iterate through dict that are the values of the defaultdict
            items_as_dct:dict = dict(item)
            for key, value in items_as_dct.items() and code in datacontainer_cleaned:
                if key in code['Coderiung']:
                    file.write(f'{value}x\t{key}\n') #write every item and the number of its occurance in a new line
        file.write('\n') #write a new line to have some space to the next  file.write(f'{key}\n')



 
      
def data_sorter(lst, dct) -> None:
    categories_all: list = []
    subs = defaultdict(list)
    #find the categories
    for i in range(len(lst)-3): #offset due to source-excel-sheet
        i=3+i
        line: str= str(lst[i]) #read each line and convert it into a string
        categories_all.append(line[0:3]) #read the first 3 letters of the code, to generate a list with the abbreviations in the codes)
        categories: list = list(dict.fromkeys(categories_all)) #condense list to the categories only
    for i in range(len(lst)-3): #offset due to source-excel-sheet
        i=3+i
        line: str= str(lst[i]) #read each line and convert it into a string
        for ii in range(len(categories)):
            if line[0:3] in categories[ii]:
                subs[categories[ii]].append(line) #generate multivalue defaultdicts, one for each category,values are all the codes with matching
    for i in range(len(categories)):
        subs_count = Counter(subs[categories[i]]) #count the occurances of each code
        subs_count_temp: dict = dict(subs_count) #transform counted defaultdict to standard dict
        subs[categories[i]] = subs_count_temp #replace old value-set with new values-set
    with open (text_path, 'w') as file: #write textfile
        for key, value_dict in subs.items(): #iterate through subs 
            file.write(f'{key}\n') #write key in one line
            for item, count in value_dict.items(): #iterate through dict that are the values of the defaultdict
                file.write(f'  {count}: {item}\n') #write every item and the number of its occurance in a new line
            file.write('\n') #write a new line to have some space to the next  file.write(f'{key}\n')
    #match categories
    for i in range(len(categories)):
        for key, value in dct.items():
            if categories[i] in key:
                print(value)
    print(kurztext)
    
data_sorter(data_frame, et)
"""
