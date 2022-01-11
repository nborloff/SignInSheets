import pandas as pd
from pprint import pprint
from re import search
import re

'''Read Excel Spreadsheet - Only Relevant Columns'''
df = pd.read_csv('https://api.codereadr.com/share/45d80f27f0f12c8402f2e2371c849990', usecols = ['User Name', 'Barcode', 'Result'])

'''Convert Datafram to List'''
master_list = df.values.tolist()

'''Reverse List'''
master_list.reverse()

'''Declare Separate Lists for Each Location'''
child_list = []
LLRC = []
Library = []
MESA = []
Fitness = []


'''Separate Data by Location + Formatting'''
for location, SID, check in master_list:
    
    if search("IN", check): # Add entry that specifies IN or OUT before formatting
        status = "IN"
    else:
        status = "OUT"
    
    new = re.sub("[^0-9]", "", check) # trim excess info from timestamp
    formatted0 = new[:4] + "-" + new[4:] # then format date/time
    formatted1 = formatted0[:7] + "-" + formatted0[7:]
    formatted2 = formatted1[:10] + " " + formatted1[10:]
    formatted3 = formatted2[:13] + ":" + formatted2[13:]
    formatted4 = formatted3[:16] + ":" + formatted3[16:]
    child_list.append([location, SID, formatted4, status])

for location, SID, check, status in child_list: # sort into lists by location
    if location == "LLRC":
        LLRC.append([location, SID, check, status])
    elif location == "MendocinoCollege-Library":
        Library.append([location, SID, check, status])
    elif location == "MESA-MC":
        MESA.append([location, SID, check, status])
    elif location == "Fitness":
        Fitness.append([location, SID, check, status])

'''Need to export to spreadsheet at this point'''

LLRC_NEW = []

for location, SID, check, status in LLRC:
    format = re.sub("[^0-9]", "", check)
    format1 = format[8:]
    LLRC_NEW.append([location, SID, check, status, format1])

'''Add up time totals'''
LLRC_Dict = {} # total time spent in lab
LLRC_Dict_Count = {} # SID attached to variable
Library_Dict = {}
MESA_Dict = {}
Fitness_Dict = {}

for location, SID, check, status, stamp in LLRC_NEW:
    LLRC_Dict[SID] = 0

for location, SID, check, status, stamp in LLRC_NEW:
    
    if status == 'IN':
        LLRC_Dict_Count[SID] = stamp

    else:
        LLRC_Dict[SID] = LLRC_Dict[SID] + (int(stamp) - int(LLRC_Dict_Count[SID]))
         
pprint(LLRC_Dict)        
        
