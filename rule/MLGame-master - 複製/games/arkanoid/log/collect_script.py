import pickle
import os 

allList = os.listdir()
reList = []

for name in allList:
    if('ml_EASY'in name):
        reList.append(name)
    
print(reList) 
print(len(reList))

pickle.dump(reList, open("list.pickle", 'wb'))
