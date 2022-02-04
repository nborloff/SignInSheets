from doctest import master
from queue import Empty
import string
import pandas as pd
from pprint import pprint
from re import I, search
import re
from datetime import datetime
import math
import numpy as np

'''Read Excel Spreadsheet - Only Relevant Columns'''
df = pd.read_csv('https://api.codereadr.com/share/45d80f27f0f12c8402f2e2371c849990', usecols = ['User Name', 'Barcode', 'Result', 'Timestamp Scanned', 'Answer 1'])

df.rename(columns={'Answer 1': 'Answer'}, inplace=True)
df1 = df.replace(np.nan, 'Other', regex=True)
print(df1)
'''Convert Datafram to List'''
master_list = df.values.tolist()

'''Reverse List'''
master_list.reverse()

'''Declare Separate Lists for Each Location'''
child_list = []
LLRC = []
MESA = []
Fitness = []

'''Separate Data by Location + Formatting'''
for location, SID, in_out, t_stamp, LLRC_Prog in master_list:
    
    if search("IN", in_out): # Add entry that specifies IN or OUT before formatting
        in_out = "IN"
    else:
        in_out = "OUT"

    child_list.append([location, SID, in_out, t_stamp, LLRC_Prog])


for location, SID, in_out, t_stamp, LLRC_Prog in master_list:
    
    str(LLRC_Prog)
    
    child_list.append([location, SID, in_out, t_stamp, LLRC_Prog])

for location, SID, in_out, t_stamp, LLRC_Prog in child_list: # sort into lists by location
    if location == "LLRC":
        LLRC.append([location, SID, in_out, t_stamp, LLRC_Prog])
    elif location == "MESA-MC":
        MESA.append([location, SID, in_out, t_stamp, LLRC_Prog])
    elif location == "Fitness":
        Fitness.append([location, SID, in_out, t_stamp, LLRC_Prog])

'''Export Raw but Formatted Data to Spreadsheet'''
LLRC_df = pd.DataFrame(LLRC, columns = ['Location', 'SID', 'in_out', 'Timestamp', 'Program'])
MESA_df = pd.DataFrame(MESA, columns = ['Location', 'SID', 'in_out', 'Timestamp', 'Program'])
Fitness_df = pd.DataFrame(Fitness, columns = ['Location', 'SID', 'in_out', 'Timestamp', 'Program'])

LLRC_df.to_csv('LLRC.csv', index=False)
MESA_df.to_csv('MESA.csv', index=False)
Fitness_df.to_csv('Fitness.csv', index=False)

'Declare Lists for LLRC Programs'
Math_Lab = []
Student_Computers = []
EDU_500 = []
Study_Room = []
Other = []

'''Separates LLRC by Program'''

'''for location, SID, in_out, t_stamp, LLRC_Prog in LLRC:
    if search("Lab", LLRC_Prog):
        Math_Lab.append([SID, t_stamp, LLRC_Prog, in_out])
    elif search("Computers", LLRC_Prog):
        Student_Computers.append([SID, t_stamp, LLRC_Prog, in_out])
    elif search("Peer", LLRC_Prog):
        EDU_500.append([SID, t_stamp, LLRC_Prog, in_out])
    elif search("Room", LLRC_Prog):
        Study_Room.append([SID, t_stamp, LLRC_Prog, in_out])
    else:
        Other.append([SID, t_stamp, LLRC_Prog, in_out])'''


#pprint(Math_Lab)
