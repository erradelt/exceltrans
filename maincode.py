import os
import pandas as pd
from collections import defaultdict

import filepathgen as fg #module that generates filpath to the current directory
from equipment import equipment_types as et #dict containing the types of equipment

class Converter:
    def __init__(self, source):
        self.source = source
        self.xls_reader()
        self.container()
        self.cat_extract()
    
    def xls_reader(self):
        df = pd.read_excel(self.source, header=1) #header = 1 -> first row will be ignored (default: header = 0)
        return df
    
    def container(self):
        datacontainer: list = []
        i_lst: list = [] # list thats used to save all the indices of rows without content
        for index, row in self.xls_reader().iterrows():
        # Convert the row to a dictionary, for instance
            dataset = row.to_dict()
            if pd.isna(row['Familie']): #pd.isna is build in pandas function to check for empty cells. the line checks for an empty cell in every row of the column 'Familie'
                i_lst.append(index)
            datacontainer.append(dataset)
        datacontainer_cleaned = [item for i, item in enumerate(datacontainer) if i not in i_lst] # generate new list without empty items
        return datacontainer_cleaned

    def cat_extract(self):
        categories_all: list = []
        for data in self.container():
            cat: str = str(data['Art'])
            categories_all.append(cat)
            
        categories: list = list(dict.fromkeys(categories_all)) # delete doublicates
        types_raw: list = []
        for art in self.container():
            cat_temp: str = str(art['Art']) #temporarily extract the type of each item
            if cat_temp in categories_all: #if type matches a category add the code of the item to the list 'types_raw'
                types_raw.append(str(art['Codierung']))
        print(types_raw)
        return types_raw