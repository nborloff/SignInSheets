from doctest import master
from queue import Empty
import string
import pandas as pd
from pprint import pprint
from re import I, search
import re
from datetime import datetime
import numpy as np
from pathlib import Path
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow
import sys

'''define application'''
def window():
    app = QApplication(sys.argv)
    win = QMainWindow()
    win.setGeometry(200, 200, 500, 500)
    win.setWindowTitle("LLRC Attendance")

    label = QtWidgets.QLabel(win)
    label.setText("MESA")
    label.move(50,50)

    win.show()
    sys.exit(app.exec_())

'''Read Excel Spreadsheet - Only Relevant Columns'''
df = pd.read_csv('API_KEY_GOES_HERE', usecols = ['User Name', 'Barcode', 'Result', 'Timestamp Scanned', 'Answer 1'])

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
MESA_Test = []

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

for location, SID, in_out, t_stamp, LLRC_Prog in MESA:
    if LLRC_Prog == "Other":
        MESA_Test.append([SID, t_stamp, LLRC_Prog, in_out])
    else:
        print("Problem")

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
                
'''First IN in list, we create a new entry in a new dictionary, set flag to true.
If we hit a second in that means the student hasn't logged out and we add 60 minutes to their
sheet and then set the flag to false. If we hit an IN and the flag is false, we set it to true and
wait for either a second IN (previous case) or an integer. If we hit an integer we add the number
to their total and then await an OUT. When we hit the OUT we se the flag to false. '''


Final_Dict = {}
flag = False

def final_calc(dict):
    for key, val in dict.items():
        for i in val:
            if  i == "IN" and key not in Final_Dict:
                Final_Dict.update({key: [0]})
                flag = True   
            elif i == "IN" and flag == True:
                Final_Dict[key] += [240]
                flag = False
            elif i == "IN" and flag == False:
                flag = True
            elif i == "OUT":
                flag = False
            else:
                Final_Dict[key] += [i]

'''Must deal with last entry being an IN with no OUT'''


                
'''This sums up the total of all the numbers in the values list, converts it to a dataframe,
and then send it to a CSV.'''

def export(dict):
    global data_frame
    for key in dict:
        dict[key] = [sum(dict[key])]
    
    dict_items = dict.items()
    
    dict_list = list(dict_items)
    
    data_frame = pd.DataFrame(dict_list)
    
    data_frame.columns = ['SID', 'Total Time']
    data_frame['Total Time'] = data_frame['Total Time'].explode().astype(int)
    check_this = pd.to_datetime(data_frame['Total Time'], unit='m').dt.strftime('%H:%M')
    
    result = pd.concat([data_frame, check_this], axis=1)
    pprint(result)
    
    filepath = Path('finished/out.csv')
    filepath.parent.mkdir(parents=True, exist_ok=True)
    result.to_csv(filepath, index=False)


to_dict(Other)
check_valid(Count_List)
final_calc(Total_Dict)

export(Final_Dict)
window()
