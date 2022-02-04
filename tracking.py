import string
import pandas as pd
from pprint import pprint
from re import I, search
import re
from datetime import datetime

'''Read Excel Spreadsheet - Only Relevant Columns'''
df = pd.read_csv('https://api.codereadr.com/share/45d80f27f0f12c8402f2e2371c849990', usecols = ['User Name', 'Barcode', 'Result', 'Timestamp Scanned', 'Answer 1'])

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

for location, SID, in_out, t_stamp, LLRC_Prog in child_list: # sort into lists by location
    if location == "LLRC":
        LLRC.append([location, SID, in_out, t_stamp, LLRC_Prog])
    elif location == "MESA-MC":
        MESA.append([location, SID, in_out, t_stamp])
    elif location == "Fitness":
        Fitness.append([location, SID, in_out, t_stamp])

'''Export to a spreadsheet at this point'''

LLRC_df = pd.DataFrame(LLRC, columns = ['Location', 'SID', 'in_out', 'Timestamp', 'Program'], dtype = float)
MESA_df = pd.DataFrame(MESA, columns = ['Location', 'SID', 'in_out', 'Timestamp'], dtype = float)

LLRC_df.to_csv('LLRC.csv', index=False)
MESA_df.to_csv('MESA.csv', index=False)

'''Add up time totals'''
EDU_List = []
Other_List = []

'''Separates LLRC Hours -> EDU 500 one list, all other go to another list'''
def split(die_Lage):
    for location, SID, in_out, t_stamp, LLRC_Prog in die_Lage:
        if LLRC_Prog == 'EDU 500':
            EDU_List.append([SID, t_stamp, LLRC_Prog, in_out])
        else:
            Other_List.append([SID, t_stamp, LLRC_Prog, in_out])

split(LLRC)


Count_List = {}

'''Puts list into dictionary with key as SID and values as timestamps'''
def fun(zeit):
    for SID, t_stamp, LLRC_Prog, in_out in zeit:
        if SID not in Count_List:
            Count_List[SID] = [t_stamp]
            Count_List[SID].append(in_out)
        else:
            Count_List[SID].append(t_stamp)
            Count_List[SID].append(in_out)

fun(EDU_List)
fun(Other_List)

pprint(Count_List)

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
            
            if i[0:11] == temp[0:11]:
                tstamp1 = datetime.strptime(i, fmt)
                tstamp2 = datetime.strptime(temp, fmt)
                difference = int(round(abs((tstamp2 - tstamp1).total_seconds()) / 60))      
                Total_Dict[key] += [difference]
                Total_Dict[key] += ["OUT"]
                
            elif key in Total_Dict:    
                Total_Dict[key] += ["IN"]
                temp = i
                
            else:
                temp = i
                Total_Dict.update({key: ["IN"]}) #First time SID running through


check_valid(Count_List)


temp_keys = []
temp_keys = list(Total_Dict.keys())

temp_values = []
temp_values = list(Total_Dict.values())

final_count = 0
in_check = bool
out_check = bool

for lists in temp_values:
    for value in lists:
        if value == 6000:
            final_count += 60
            in_check == True
            out_check  == False
        elif value == 5000:
            final_count -= 60
            out_check == True
            in_check == False
        else:
            final_count == value



    






  
            
        

    




        
    

