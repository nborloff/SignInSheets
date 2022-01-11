import pandas as pd
from pprint import pprint
from re import search
import re

'''Read Excel Spreadsheet - Only Relevant Columns'''
df = pd.read_csv('https://api.codereadr.com/share/5aa76baae4f197a6dbab56e11e144dd2', usecols = ['User Name', 'Barcode', 'Result'])

'''Convert Datafram to List'''
master_list = df.values.tolist()

'''Reverse List'''
master_list.reverse()

'''Declare Separate Lists for Each Location'''
LLRC = []
Library = []

'''Separate Data by Location + Initial Formatting'''
for location, SID, check in master_list:
    if location == "LLRC":
        if search("IN", check):
            status = "IN"
        else:
            status = "OUT"
        new = re.sub("[^0-9]", "", check) # trim excess info from timestamp
        formatted0 = new[:4] + "-" + new[4:] # then format date/time
        formatted1 = formatted0[:7] + "-" + formatted0[7:]
        formatted2 = formatted1[:10] + " " + formatted1[10:]
        formatted3 = formatted2[:13] + ":" + formatted2[13:]
        formatted4 = formatted3[:16] + ":" + formatted3[16:]
        LLRC.append([location, SID, formatted4, status])
        
    elif location == "MendocinoCollege-Library":
        if search("IN", check):
            lb_status = "IN"
        else:
            lb_status = "OUT"
        new1 = re.sub("[^0-9]", "", check) # trim excess info from timestamp
        lb_formatted0 = new1[:4] + "-" + new1[4:] # then format date/time
        lb_formatted1 = lb_formatted0[:7] + "-" + lb_formatted0[7:]
        lb_formatted2 = lb_formatted1[:10] + " " + lb_formatted1[10:]
        lb_formatted3 = lb_formatted2[:13] + ":" + lb_formatted2[13:]
        lb_formatted4 = lb_formatted3[:16] + ":" + lb_formatted3[16:]
        Library.append([location, SID, lb_formatted4, lb_status])
        
pprint(LLRC)
pprint(Library)

