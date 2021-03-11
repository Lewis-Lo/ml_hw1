"""
The template of the main script of the machine learning process
"""
import random
class MLPlay:
    def __init__(self):
        """
        Constructor
        """
        self.ball_served = False
        self.preBall = [0, 1]
        self.deltaBall = [0, 0]

    # def coll(self, scene_info, X, Y):
    #     for i in scene_info['bricks']:
    #         if(X>=i[0] and X<=(i[0]+25) and Y>=i[1] and Y<=(i[1]+10)):
    #             #print("X:{}, Y:{}, BX:{}, BY:{}".format(X, Y, i[0], i[1]))
    #             return i[0]

    #     for i in scene_info['hard_bricks']:
    #         if(X>=i[0] and X<=(i[0]+25) and Y>=i[1] and Y<=(i[1]+10)):
    #             return i[0]
    #     return -999

    def nextBall(self, X, Y, dire, speed, scene_info):
        # dir : 0:右上, 1:右下, 2:左上, 3:左下    
        tempX = X
        tempY = Y
        for i in range(0, speed):
            if(dire == 0):
                tempX = tempX + 1
                tempY = tempY - 1
            elif(dire == 1):
                tempX = tempX + 1
                tempY = tempY + 1
            elif(dire == 2):
                tempX = tempX - 1
                tempY = tempY - 1
            elif(dire == 3):
                tempX = tempX - 1
                tempY = tempY + 1

            if(dire == 0):
                if(tempY <= 0):
                    return tempX, 0, 1
                elif(tempX >= 200):
                    return 195, tempY, 2
            elif(dire == 1):
                if(tempX >= 200):
                    return 195, tempY, 3
            elif(dire == 2):
                if(tempY <= 0):
                    return tempX, 0, 3
                elif(tempX <= 0):
                    return 0, tempY, 0
            elif(dire == 3):
                if(tempX <= 0):
                    return 0, tempY, 1

            for i in scene_info['bricks']:
                if(tempX>=i[0] and tempX<=(i[0]+25) and tempY>=i[1] and tempY<=(i[1]+10)):
                    if(dire == 0):
                        if(abs(tempX - (i[0] + 25)) >= abs(tempY - (i[1]+10))):
                            return tempX, i[1]+10, 1
                        else:
                            return i[0]-5, tempY, 2
                    elif(dire == 1):
                        if(abs(tempX - (i[0] + 25)) >= abs(tempY - (i[1]))):
                            return tempX, i[1]-5, 0
                        else:
                            return i[0]-5, tempY, 3
                    elif(dire == 2):
                        if(abs(tempX - (i[0] + 25)) >= abs(tempY - (i[1]+10))):
                            return tempX, i[1]+10, 3
                        else:
                            return i[0] + 25, tempY, 0
                    elif(dire == 3):
                        if(abs(tempX - (i[0] + 25)) >= abs(tempY - (i[1]))):
                            return tempX, i[1]-5, 2
                        else:
                            return i[0] + 25, tempY, 1
        return tempX, tempY, dire


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
            self.deltaBall[0] = scene_info['ball'][0] - self.preBall[0]
            self.preBall[0] = scene_info['ball'][0]
            self.deltaBall[1] = scene_info['ball'][1] - self.preBall[1]
            self.preBall[1] = scene_info['ball'][1]
            # print(self.deltaBall)
            destinationX = scene_info['ball'][0]
            destinationY = scene_info['ball'][1]

            speed = abs(self.deltaBall[0])
            dire = 10

            if(self.deltaBall[0] > 0 and self.deltaBall[1] < 0):
                dire = 0
            elif(self.deltaBall[0] > 0 and self.deltaBall[1] > 0):
                dire = 1
            elif(self.deltaBall[0] < 0 and self.deltaBall[1] < 0):
                dire = 2
            elif(self.deltaBall[0] < 0 and self.deltaBall[1] > 0):
                dire = 3

            for i in range(1, 200):
                destinationX, destinationY, dire = self.nextBall(destinationX, destinationY, dire, speed, scene_info)
                if(destinationY >= 400):
                    break


            print(destinationX, scene_info['ball'][0])

            if(abs((scene_info['platform'][0] + 20) - destinationX) < random.randint(9, 11)):
                command = "NONE"
            elif(scene_info['platform'][0]+20 > destinationX):
                command = "MOVE_LEFT"
            else:
                command = "MOVE_RIGHT"

                    


        # print(scene_info)
                


        return command

    def reset(self):
        """
        Reset the status
        """
        self.ball_served = False
