import os
import pandas as pd
import glob

os.chdir(os.getcwd())
for f in glob.glob("Filter_*.csv"):
    os.remove(f)

print ("running file at "+os.getcwd())

#  Show all indices in a list - function
def all_indices(value, qlist):
    indices = []
    idx = -1
    while True:
        try:
            idx = qlist.index(value, idx+1)
            indices.append(idx)
        except ValueError:
            break
    return indices

filter = pd.read_table('temp_filter.tab')
filter[:] = filter[:].astype(str) 

Pd3 = filter.Prodgroup3[0].split(",")
Opr = filter.Operation[0].split(",")
pd.DataFrame(data={'Operation' : Opr}).to_csv("Filter_"+'Operation.csv', index = False)
BSelect = filter.Binselect[0].split(",")
BExclude = filter.Binexclude[0].split(",")

# Switcher LC, EF 
allLCflag = [0]
allEFflag = [0]
runLCflag = [0]
runEFflag = [0]
if len(all_indices("all", BSelect)) > 0:
    allLCflag = [1]
    allEFflag = [1]
    runLCflag = [1]
    runEFflag = [1]
elif len(all_indices("alllc", BSelect)) > 0:
    allLCflag = [1]
    runLCflag = [1]
elif len(all_indices("allef", BSelect)) > 0:
    allEFflag = [1]
    runEFflag = [1]
    
# LossCode filter
LCSelect = []
for i in BSelect:
     if i.find("all") == -1 & i.find("IB") == -1 & i.find("FB") == -1:
         LCSelect.append(i)
pd.DataFrame(data={'LCSelect' : LCSelect}).to_csv("Filter_"+'LCSelect.csv', index = False)
        
LCExclude = []
for i in BExclude:
     if i.find("IB") == -1 & i.find("FB") == -1:
         LCExclude.append(i)
pd.DataFrame(data={'LCExclude' : LCExclude}).to_csv("Filter_"+'LCExclude.csv', index = False) 

     
# IB filter
IBSelect = []
for i in BSelect:
     if i.find("IB") >= 0:
         IBSelect.append(i)
pd.DataFrame(data={'IBSelect' : IBSelect}).to_csv("Filter_"+'IBSelect.csv', index = False)
 
IBExclude = []
for i in BExclude:
     if i.find("IB") >= 0:
         IBExclude.append(i)
pd.DataFrame(data={'IBExclude' : IBExclude}).to_csv("Filter_"+'IBExclude.csv', index = False) 
        
# FB filter
FBSelect = []
for i in BSelect:
     if i.find("FB") >= 0:
         FBSelect.append(i.replace("FB",""))
pd.DataFrame(data={'FBSelect' : FBSelect}).to_csv("Filter_"+'FBSelect.csv', index = False)

FBExclude = []
for i in BExclude:
     if i.find("FB") >= 0:
         FBExclude.append(i.replace("FB",""))
pd.DataFrame(data={'FBExclude' : FBExclude}).to_csv("Filter_"+'FBExclude.csv', index = False) 

# IB slipt to FB
IBslipt = []
for i in (FBSelect + FBExclude):
    IBslipt.append(i[:-2])
pd.DataFrame(data={'IBslipt' : IBslipt}).to_csv("Filter_"+'IBslipt.csv', index = False) 

SFPFilter = [('Prodgroup3' , Pd3),
             ('allLCflag', allLCflag),
             ('allEFflag', allEFflag),
             ('runLCflag', runLCflag),
             ('runEFflag', runEFflag)
        ] 
pd.DataFrame.from_items(SFPFilter).to_csv("Filter_"+'Main.csv', index = False)