import os
import pandas as pd
import re
import openpyxl
from collections import defaultdict, Counter

import filepathgen as fg #module that generates filpath to the current directory
from equipment import equipment_types as et #dict containing the types of equipment

#setting path to file by using the module filepathgen, this only works, if the list is located in the same 
#directory as the program

#filepaths
excel_path: str = os.path.join(fg.current_directory, 'basisliste.xlsx') # path for loading excel
text_path: str = os.path.join(fg.current_directory, 'typenzahl.txt') # path for saving overview of items as .txt

df = pd. read_excel(excel_path, header=1) #header = 1 -> first row will be ignored (default: header = 0)

#read the necessary data
data_frame=df['Codierung'] #df['columnname']
data_frame_kurztext=df['Familie']

print(data_frame_kurztext)

def data_sorter(lst, dct) -> None:
    categories_all: list = []
    kurztext: list = []
    subs = defaultdict(list)
    #find the categories
    for i in range(len(lst)-3): #offset due to source-excel-sheet
        i=3+i
        line: str= str(lst[i]) #read each line and convert it into a string
        kt: str= str(data_frame_kurztext[i])
        categories_all.append(line[0:3]) #read the first 3 letters of the code, to generate a list with the abbreviations in the codes)
        kurztext.append(kt)
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


