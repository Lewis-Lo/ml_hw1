import pickle
from os import path
import numpy as np

file = open("ml_EASY_20.pickle", "rb")
log = pickle.load(file)
# print(log['ml']['scene_info'][0]['frame'])
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
    
# game result
print(log['ml']['scene_info'][len(log['ml']['scene_info']) - 1]['status'])

data = np.array([BallX, BallY, ReX, ReY, dirX, dirY, Direction, PlatformX,Command])
pickle.dump(data, open('s20', 'wb'))
# print(data)
# print(np.shape(data))
# print(data[0])

# Frames = []
# Balls = []
# Commands = []
# Platforms = []
# Bricks = []
# Hard_Bricks = []

# for i in range(0, len(log['ml']['scene_info'])):
#     Frames.append(log['ml']['scene_info'][i]['frame'])
#     Balls.append(log['ml']['scene_info'][i]['ball'])
#     Platforms.append(log['ml']['scene_info'][i]['platform'])
#     Commands.append(log['ml']['command'][i])
#     Bricks.append(log['ml']['scene_info'][i]['bricks'])
#     Hard_Bricks.append(log['ml']['scene_info'][0]['hard_bricks'])

    

#     Frame = Frames[len(Frames) - 1]
#     Ball = Balls[len(Balls) - 1]
#     Platform = Platforms[len(Platforms) - 1]
#     Brick = Bricks[len(Bricks) - 1]
#     Hard_Brick = Hard_Bricks[len(Hard_Bricks) - 1]
#     Command = Commands[len(Commands) - 1]

    

    
    #data = np.hstack((frame_ary, Ball, Platform, commands_ary))

    #print(data)



'''def get_ArkanoidData(filename):
    file = open(filename,'rb')
    log = pickle.load(file)
    Frames = []
    Balls = []
    Commands = []
    PlatformPos = []
    for sceneInfo in log:
        Frames.append(sceneInfo.frame)
        Balls.append([sceneInfo.ball[0], sceneInfo.ball[1]])
        Commands.append(str(sceneInfo.command))
        PlatformPos.append(sceneInfo.platform)

    commands_ary = np.array([Commands])
    commands_ary = commands_ary.reshape((len(Commands), 1))
    frame_ary = np.array(Frames)
    frame_ary = frame_ary.reshape((len(Frames), 1))
    data = np.hstack((frame_ary, Balls, PlatformPos, commands_ary))
    return data

if __name__ == '__main__':
    filename = path.join(path.dirname(__file__), 'manual_EASY_1_2021-03-04_15-24-10.pickle')
    data = get_ArkanoidData(filename)
    print(data)
    X = data[:, :-1]
    Y = data[:, -1]
    print(X)
    # print(Y)'''