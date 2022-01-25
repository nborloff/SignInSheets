import pandas as pd
from pprint import pprint
from re import search
import re
import datetime as dt

'''Read Excel Spreadsheet - Only Relevant Columns'''
df = pd.read_csv('https://api.codereadr.com/share/45d80f27f0f12c8402f2e2371c849990', usecols = ['User Name', 'Barcode', 'Result', 'Timestamp Scanned', 'Answer 1'])

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
for location, SID, in_out, t_stamp, LLRC_Prog in master_list:
    
    if search("IN", in_out): # Add entry that specifies IN or OUT before formatting
        status = "IN"
    else:
        status = "OUT"
    
    child_list.append([location, SID, status, t_stamp, LLRC_Prog])

for location, SID, in_out, t_stamp, LLRC_Prog in child_list: # sort into lists by location
    if location == "LLRC":
        LLRC.append([location, SID, in_out, t_stamp, LLRC_Prog])
    elif location == "MendocinoCollege-Library":
        Library.append([location, SID, in_out, t_stamp])
    elif location == "MESA-MC":
        MESA.append([location, SID, in_out, t_stamp])
    elif location == "Fitness":
        Fitness.append([location, SID, in_out, t_stamp])

'''Export to a spreadsheet at this point'''


'''Add up time totals'''
EDU_List = []
Other_List = []

def fun(die_Lage):
    for location, SID, in_out, t_stamp, LLRC_Prog in die_Lage:
        if LLRC_Prog == 'EDU 500':
            EDU_List.append([SID, t_stamp, LLRC_Prog])
        else:
            Other_List.append([SID, t_stamp, LLRC_Prog])

fun(LLRC)

Count_List = {}

def fun(zeit):
    for SID, t_stamp, LLRC_Prog in zeit:
        if SID not in Count_List:
            Count_List[SID] = [t_stamp]
        else:
            Count_List[SID].append(t_stamp)

fun(EDU_List)

pprint(Count_List)