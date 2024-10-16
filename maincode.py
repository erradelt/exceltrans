import os
import pandas as pd
from collections import defaultdict

import filepathgen as fg #module that generates filpath to the current directory
from equipment import equipment_types as et #dict containing the types of equipment

class Converter:
    def __init__(self, source, new_name):
        self.source = source
        self.new_name = new_name
        self.xls_reader()
        self.container()
        self.cat_extract_and_count()
        self.types_per_room()
        self.exporter()

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

    def cat_extract_and_count(self):
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
                    
        types: dict = {}
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
        return types_sorted
    
    def types_per_room(self):
        rooms = defaultdict(lambda: defaultdict(int))
        for item in self.container():
            room_name = item['MEP-Raum: Name']
            code = item['Codierung']
            rooms[room_name][code] += 1
        return rooms
    
    def exporter(self):
        self.new_name
        out_to_excel: list = []
        for key, list_of_dicts in self.cat_extract_and_count().items():
            for item in list_of_dicts:
                for sub_key, value in item.items():
                    # Create a list of rooms where this code occurs and how many times it occurs in each room
                    room_info = []
                    for room_name, room_codes in self.types_per_room().items():
                        if sub_key in room_codes:
                            room_info.append(f"{room_name}: {room_codes[sub_key]}")

                    room_info_str = "; ".join(room_info)  # Join all room info into one string
                    out_to_excel.append({'Categorie': key, 'Code': sub_key, 'Menge': value, 'Rooms': room_info_str}) 
        

        of = pd.DataFrame(out_to_excel)
        
        with pd.ExcelWriter(f'{self.new_name}.xlsx', engine='xlsxwriter') as writer:
            for i in range(0, len(of), 100):
                of.iloc[i:i+100].to_excel(writer, sheet_name='Massen-LV', startrow=i, index=False, header=i == 0)
                                     
    
    