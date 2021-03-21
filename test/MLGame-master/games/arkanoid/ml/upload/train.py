import pickle
import os 
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn import svm
from sklearn.tree import DecisionTreeClassifier
from sklearn import ensemble, preprocessing, metrics
from sklearn import preprocessing
from sklearn import linear_model

################## collect file names ##################
allList = os.listdir()
reList = []

for name in allList:
    if('ml_EASY'in name):
        reList.append(name)
    
print(reList) 
print(len(reList))

pickle.dump(reList, open("list.pickle", 'wb'))

################### get feature ##################
obj = pickle.load(open("list.pickle", "rb"))
index = 1
print(obj)
for files in obj:

    f = open(files, "rb")
    log = pickle.load(f)

    Frame = np.zeros([len(log['ml']['scene_info'])])
    BallX = np.zeros([len(log['ml']['scene_info'])])
    BallY = np.zeros([len(log['ml']['scene_info'])])
    Direction = np.zeros([len(log['ml']['scene_info']) - 1])
    PlatformX = np.zeros([len(log['ml']['scene_info'])])
    ReX = np.zeros([len(log['ml']['scene_info'])])
    ReY = np.zeros([len(log['ml']['scene_info'])])
    Command = np.zeros([len(log['ml']['scene_info'])])

    print(np.shape(Frame))
    for i in range(0, len(log['ml']['scene_info'])):
        t=0
        Frame[i] = log['ml']['scene_info'][i]['frame']
        BallX[i] = log['ml']['scene_info'][i]['ball'][0]
        BallY[i] = log['ml']['scene_info'][i]['ball'][1]
        PlatformX[i] = log['ml']['scene_info'][i]['platform'][0]
        ReX[i] = BallX[i] - PlatformX[i]
        ReY[i] = BallY[i] - log['ml']['scene_info'][i]['platform'][1]
        if(log['ml']['command'][i] == 'NONE'):
            Command[i] = 0
        elif(log['ml']['command'][i] == 'MOVE_LEFT'):
            Command[i] = 1
        elif(log['ml']['command'][i] == 'MOVE_RIGHT'):
            Command[i] = 2

    dirX = np.zeros([len(log['ml']['scene_info']) - 1])
    dirY = np.zeros([len(log['ml']['scene_info']) - 1])

    for i in range(0, len(log['ml']['scene_info']) - 1):
        dirX[i] = BallX[i+1] - BallX[i]
        dirY[i] = BallY[i+1] - BallY[i]
        if(dirX[i] > 0 and dirY[i] > 0):
            #右下
            Direction[i] = 0
        elif(dirX[i] > 0 and dirY[i] < 0):
            #右上
            Direction[i] = 1
        elif(dirX[i] < 0 and dirY[i] > 0):
            #左上
            Direction[i] = 2
        elif(dirX[i] < 0 and dirY[i] < 0):
            #左下
            Direction[i] = 3
        
    Command = Command[:-1]
    PlatformX = PlatformX[:-1]
    BallX = BallX[:-1]
    BallY = BallY[:-1]
    ReX = ReX[:-1]
    ReY = ReY[:-1]

    num_bricks = 0
    num_hard_bricks = 0

    for i in log['ml']['scene_info'][0]['bricks']:
        num_bricks = num_bricks + 1
    for i in log['ml']['scene_info'][0]['hard_bricks']:
        num_hard_bricks = num_hard_bricks + 1

    bricks = np.zeros([len(log['ml']['scene_info'])])
    hard_bricks = np.zeros([len(log['ml']['scene_info'])])

    for i in range(0, len(log['ml']['scene_info'])):
        bricks[i] = num_bricks
        hard_bricks[i] = num_hard_bricks
        
    bricks = bricks[:-1]
    hard_bricks = hard_bricks[:-1]

    # game result
    print(log['ml']['scene_info'][len(log['ml']['scene_info']) - 1]['status'])

    data = np.array([BallX, BallY, ReX, ReY, dirX, dirY, Direction, PlatformX, bricks, hard_bricks, Command])
    print(data)
    pickle.dump(data, open('u{}.pickle'.format(str(index)), 'wb'))
    index = index + 1
################### train ##################


files = ['', '', '', '', '', '', '', '', '', '', 
         '', '', '', '', '', '', '', '', '', '', 
         '', '', '', '', '', '', '', '', '', '', 
         '', '', '', '', '', '', '', '', '', '', 
         '', '', '', '', '', '', '', '', '', '', 
         '', '', '', '', '', '', '', '', '', '', 
         '', '', '', '', '', '', '', '', '', '', 
         '', '', '', '', '', '', '', '', '', '', 
         '', '', '', '', '', '', '', '', '', '', 
         '', '', '', '', '', '', '', '', '', '', 
         '', '', '', '', '', '', '', '', '', '', 
         '', '', '', '', '', '', '', '', '', '', 
         '', '', '', '', '', '', '', '', '', '', 
         '', '', '', '', '', '', '', '', '', '', 
         '', '', '', '', '', '', '', '', '', '', 
         '', '', '', '', '', '', '', '', '', '', 
         '', '', '', '', '', '', '', '', '', '', 
         '', '', '', '', '', '', '', '', '', '', 
         '', '', '', '', '', '', '', '', '', '', 
         '', '', '', '', '', '', '', '', '', '', 
         '', '', '', '', '', '', '', '', '', '', 
         '', '', '', '', '', '', '', '', '', '', 
         '', '', '', '', '', '', '', '', '', '', 
         '', '', '', '', '', '', '', '', '', '', 
         '', '', '', '', '', '', '', '', '', '', 
         '', '', '', '', '', '', '', '', '', '', 
         '', '', '', '', '', '', '', '', '', '', 
         '', '', '', '', '', '', '', '', '', '', 
         '', '', '', '', '', '', '', '', '', '', 
         '', '', '', '', '', '', '', '', '', '', 
         '', '', '', '', '', '', '', '', '', '', 
         '', '', '', '', '', '', '', '', '', '', 
         '', '', '', '', '', '', '', '', '', '', 
         '', '', '', '', '', '', '', '', '', '', 
         '', '', '', '', '', '', '', '', '', '', 
         '', '', '', '', '', '', '', '', '', '', 
         '', '', '', '', '', '', '', '', '', '', 
         '', '', '', '', '', '', '', '', '', '', 
         '', '', '', '', '', '', '', '', '', '', 
         '', '', '', '', '', '', '', '', '', '', 
         '', '', '', '', '', '', '', '', '', '', 
         '', '', '', '', '', '', '', '', '', '', 
         '', '', '', '', '', '', '', '', '', '', 
         '', '', '', '', '', '', '', '', '', '', 
         '', '', '', '', '', '', '', '', '', '', 
         '', '', '', '', '', '', '', '', '', '', 
         '', '', '', '', '', '', '', '', '', '', 
         '', '', '', '', '', '', '', '', '', '', 
         '', '', '', '', '', '', '', '', '', '', 
         '', '', '', '', '', '', '', '', '', '', 
         '', '', '', '', '', '', '', '', '', '', 
         '', '', '', '', '', '', '', '', '', '', 
         '', '', '', '', '', '', '', '', '', '', 
         '', '', '', '', '', '', '', '', '', '', 
         '', '', '', '', '', '', '', '', '', '', 
         '', '', '', '', '', '', '', '', '', '', 
         '', '', '', '', '', '', '', '', '', '', 
         '', '', '', '', '', '', '', '', '', '', 
         '', '', '', '', '', '', '', '', '', '', 
         '', '', '', '', '', '', '', '', '', '', 
         '', '', '', '', '', '', '', '', '', '', 
         '', '', '', '', '', '', '', '', '', '', 
         '', '', '', '', '', '', '', '', '', '', 
         '', '', '', '', '', '', '', '', '', '', 
         '', '', '', '', '', '', '', '', '', '', 
         '', '', '', '', '', '', '', '', '', '', 
         '', '', '', '', '', '', '', '', '', '', 
         '', '', '', '', '', '', '', '', '', '', 
         '', '', '', '', '', '', '', '', '', '', 
         '', '', '', '', '', '', '', '', '', '', 
         '', '', '', '', '', '', '', '', '', '', 
         '', '', '', '', '', '', '', '', '', '']

for index in range(0, 3):
    files[index] = ("u{}.pickle".format(str(index+1)))

data = pickle.load(open(files[0], 'rb'))

for index in files[0:2]:
    temp = pickle.load(open(index, 'rb'))
    data = np.hstack((data, temp))

data = data.T
dataX = data[:, [0, 1, 2, 3, 4, 5, 6, 7]]
dataY = data[:, 10]

print(dataX)

X_train, X_test, Y_train, Y_test = train_test_split(dataX, dataY, test_size = 0.3)

knn = KNeighborsClassifier(n_neighbors=3)
knn.fit(X_train, Y_train)

print(knn.predict(X_test))
print(Y_test)
print(knn.score(X_test, Y_test))

pickle.dump(knn, open('model_s4.pickle', 'wb'))

dtc = tree = DecisionTreeClassifier(criterion = 'entropy', max_depth=40, random_state=3)
dtc.fit(X_train, Y_train)
print(dtc.score(X_test, Y_test))
pickle.dump(dtc, open('dtc_s4.pickle', 'wb'))



