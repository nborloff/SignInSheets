from doctest import master
from queue import Empty
import string
import pandas as pd
from pprint import pprint
from re import I, search
import re
from datetime import datetime
import numpy as np

'''Read Excel Spreadsheet - Only Relevant Columns'''
df = pd.read_csv('https://api.codereadr.com/share/45d80f27f0f12c8402f2e2371c849990', usecols = ['User Name', 'Barcode', 'Result', 'Timestamp Scanned', 'Answer 1'])

'''Fill in empty cells to avoid later errors'''
df.rename(columns={'Answer 1': 'Answer'}, inplace=True)
df1 = df.replace(np.nan, 'Other', regex=True)

'''Convert Datafram to List'''
master_list = df1.values.tolist()

'''Reverse List'''
master_list.reverse()

'''Declare Separate Lists for Each Location'''
child_list = []
LLRC = []
MESA = []
Fitness = []

'''Simplify IN/OUT Flag'''
for location, SID, in_out, t_stamp, LLRC_Prog in master_list:
    if search("IN", in_out): 
        in_out = "IN"
    else:
        in_out = "OUT"
    child_list.append([location, SID, in_out, t_stamp, LLRC_Prog])

'''Sort into separate lists by location'''
for location, SID, in_out, t_stamp, LLRC_Prog in child_list: 
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

'''Declare Lists for LLRC Programs'''
Math_Lab = []
Student_Computers = []
Math_EDU_500 = []
English_EDU_500 = []
Study_Room = []
DRC_Testing = []
Other = []
#MESA = [FULL OF STUFF]
#Fitness = [FULL OF STUFF]

'''Separates LLRC List by Program'''
for location, SID, in_out, t_stamp, LLRC_Prog in LLRC:
    if LLRC_Prog == "Faculty Math Lab: 540":
        Math_Lab.append([SID, t_stamp, LLRC_Prog, in_out])
    elif LLRC_Prog == "Math Lab: 540":
        Math_Lab.append([SID, t_stamp, LLRC_Prog, in_out])
    elif LLRC_Prog == "Student Computers":
        Student_Computers.append([SID, t_stamp, LLRC_Prog, in_out])
    elif LLRC_Prog == "Peer-Tutor Math Tutor: EDU 500":
        Math_EDU_500.append([SID, t_stamp, LLRC_Prog, in_out])
    elif LLRC_Prog == "Peer-Tutor English Tutor: EDU 500":
        English_EDU_500.append([SID, t_stamp, LLRC_Prog, in_out])
    elif LLRC_Prog == "EDU 500": # we can remove this one next month
        English_EDU_500.append([SID, t_stamp, LLRC_Prog, in_out])
    elif LLRC_Prog == "Study Room":
        Study_Room.append([SID, t_stamp, LLRC_Prog, in_out])
    elif LLRC_Prog == "DRC Testing":
        DRC_Testing.append([SID, t_stamp, LLRC_Prog, in_out])
    else:
        Other.append([SID, t_stamp, LLRC_Prog, in_out])

Count_List = {}

'''Puts list into dictionary with key as SID and values as timestamps'''
def to_dict(zeit):
    for SID, t_stamp, LLRC_Prog, in_out in zeit:
        if SID not in Count_List:
            Count_List[SID] = [t_stamp]
            Count_List[SID].append(in_out)
        else:
            Count_List[SID].append(t_stamp)
            Count_List[SID].append(in_out)

to_dict(Math_Lab)
# pprint(Count_List)
'''Calculates number of minutes per session per student - flags students
who signed in but didn't sign out'''

'''For the following function: Proper output is an integer sandwiched between
an 'IN' and an 'OUT'. Double 'INs', solo 'INs', and double 'Outs' all signify
that the student didn't sign out properly and must be dealt with computationally
according to the wishes of the manager of the department'''

Total_Dict = {}

fmt = '%Y-%m-%d %H:%M:%S'
def check_valid(Zeit_Worterbuch):
    temp = ""
    for key, val in Zeit_Worterbuch.items():
        for i in val:
            if i == "IN":
                Total_Dict[key] += ["IN"]
            elif i == "OUT":
                Total_Dict[key] += ["OUT"]    
            elif key not in Total_Dict:
                temp = i
                Total_Dict.update({key: ["IN"]})
            
            
            elif i[0:11] == temp[0:11]:
                tstamp1 = datetime.strptime(i, fmt)
                tstamp2 = datetime.strptime(temp, fmt)
                difference = int(round(abs((tstamp2 - tstamp1).total_seconds()) / 60))      
                Total_Dict[key] += [difference]
                
                
            elif key in Total_Dict:    
                
                temp = i
                


check_valid(Count_List)

pprint(Total_Dict)

