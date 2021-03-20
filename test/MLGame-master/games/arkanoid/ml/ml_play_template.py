"""
The template of the main script of the machine learning process
"""
import random
import pickle
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
import os
class MLPlay:
    def __init__(self):
        """
        Constructor
        """
        self.ball_served = False
        self.preBall = [0, 1]
        self.deltaBall = [0, 0]
        self.num_bricks = 0
        self.num_hard_bricks = 0
        self.spos = 0
        with open(os.path.join(os.path.dirname(__file__), 'modelo_8.pickle'), 'rb') as f:
            self.model = pickle.load(f)
        with open(os.path.join(os.path.dirname(__file__), 'model_s4.pickle'), 'rb') as f:
            self.model_s4 = pickle.load(f)    

    def update(self, scene_info):
        """
        Generate the command according to the received `scene_info`.
        """
        # Make the caller to invoke `reset()` for the next round.
        if (scene_info["status"] == "GAME_OVER" or
            scene_info["status"] == "GAME_PASS"):
            return "RESET"

        if not self.ball_served:

            if(scene_info['platform'][0] < self.spos):
                command = "MOVE_RIGHT"
                print(scene_info['platform'][0])
            else:
                command = "SERVE_TO_LEFT"
                self.ball_served = True


            #### s4 ####
            if(scene_info['frame'] == 0):
                self.num_bricks = 0
                self.num_hard_bricks = 0
                for i in scene_info['bricks']:
                    self.num_bricks = self.num_bricks + 1
                for i in scene_info['hard_bricks']:
                    self.num_hard_bricks = self.num_hard_bricks + 1
            if(self.num_bricks == 96):
                self.ball_served = True
            command = "SERVE_TO_LEFT"
            if(scene_info['platform'][0] < 20):
                command = "MOVE_RIGHT"
                self.ball_served = False
            #### s4 ####

            


        else:
            command = "MOVE_RIGHT"
            # model = pickle.load(open('modelo_2.pickle', 'rb'))

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

            # if(scene_info['frame'] == 1):
            #     self.num_bricks = 0
            #     self.num_hard_bricks = 0
            #     for i in scene_info['bricks']:
            #         self.num_bricks = self.num_bricks + 1
            #     for i in scene_info['hard_bricks']:
            #         self.num_hard_bricks = self.num_hard_bricks + 1


            # print(self.num_bricks, self.num_hard_bricks)

            test = np.zeros((1, 10))
            test[0, 0] = BallX
            test[0, 1] = BallY
            test[0, 2] = ReX
            test[0, 3] = ReY
            test[0, 4] = dirX
            test[0, 5] = dirY
            test[0, 6] = Direction
            test[0, 7] = scene_info['platform'][0]
            test[0, 8] = self.num_bricks
            test[0, 9] = self.num_hard_bricks

            d = test[0, [0, 1, 2, 3, 4, 5, 6, 7]].reshape(1, -1)

            if(self.num_bricks == 96):
                res = self.model_s4.predict(d)
            else:
                res = self.model.predict(d)

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
