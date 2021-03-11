"""
The template of the main script of the machine learning process
"""
import random
import pickle
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
class MLPlay:
    def __init__(self):
        """
        Constructor
        """
        self.ball_served = False
        self.preBall = [0, 1]
        self.deltaBall = [0, 0]

    def coll(self, scene_info, X, Y):
        for i in scene_info['bricks']:
            if(X>=i[0] and X<=(i[0]+25) and Y>=i[1] and Y<=(i[1]+10)):
                #print("X:{}, Y:{}, BX:{}, BY:{}".format(X, Y, i[0], i[1]))
                return i[0]

        for i in scene_info['hard_bricks']:
            if(X>=i[0] and X<=(i[0]+25) and Y>=i[1] and Y<=(i[1]+10)):
                return i[0]
        return -999
        
        

    def update(self, scene_info):
        """
        Generate the command according to the received `scene_info`.
        """
        # Make the caller to invoke `reset()` for the next round.
        if (scene_info["status"] == "GAME_OVER" or
            scene_info["status"] == "GAME_PASS"):
            return "RESET"

        if not self.ball_served:
            self.ball_served = True
            if(random.randint(0, 1) == 0):
                command = "SERVE_TO_LEFT"
            else:
                command = "SERVE_TO_RIGHT"
        else:
            command = "MOVE_RIGHT"
            model = pickle.load(open('dic2.pickle', 'rb'))

            self.deltaBall[0] = scene_info['ball'][0] - self.preBall[0]
            self.preBall[0] = scene_info['ball'][0]
            self.deltaBall[1] = scene_info['ball'][1] - self.preBall[1]
            self.preBall[1] = scene_info['ball'][1]
            
            BallX = scene_info['ball'][0]
            BallY = scene_info['ball'][1]
            ReX = BallX - scene_info['platform'][0]
            ReY = BallY - scene_info['platform'][1]
            dirX = self.deltaBall[0]
            dirY = self.deltaBall[1]
            Direction = 0

            if(dirX > 0 and dirY > 0):
                #右下
                Direction = 0
            elif(dirX > 0 and dirY < 0):
                #右上
                Direction = 1
            elif(dirX < 0 and dirY > 0):
               #左上
                Direction = 2
            elif(dirX < 0 and dirY < 0):
                #左下
               Direction = 3

            test = np.zeros((1, 5))
            #test[0, 0] = BallX
            #test[0, 1] = BallY
            test[0, 0] = ReX
            test[0, 1] = ReY
            test[0, 2] = dirX
            test[0, 3] = dirY
            test[0, 4] = Direction
            #test[0, 5] = scene_info['platform'][0]

            res = model.predict(test)
            if(res == 0):
                command = 'NONE'
            elif(res == 1):
                command = 'MOVE_LEFT'
            elif(res == 2):
                command = 'MOVE_RIGHT'

        return command

    def reset(self):
        """
        Reset the status
        """
        self.ball_served = False
