import os
import pandas
import openpyxl

import filepathgen as fg

#setting path to file by using the module filepathgen, this only works, if the list is located in the same 
#directory as the program
excel_path = os.path.join(fg.current_directory, 'basisliste.xlsx')

print(excel_path)