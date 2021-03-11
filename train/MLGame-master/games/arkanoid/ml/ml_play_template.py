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
            self.deltaBall[0] = scene_info['ball'][0] - self.preBall[0]
            self.preBall[0] = scene_info['ball'][0]
            self.deltaBall[1] = scene_info['ball'][1] - self.preBall[1]
            self.preBall[1] = scene_info['ball'][1]
            # print(self.deltaBall)
            destinationX = scene_info['ball'][0]
            destinationY = scene_info['ball'][1]
            ballY = scene_info['ball'][1]
            block = 0
            if(self.deltaBall[1] >= 0):
                for i in range(0, 100):
                    if((ballY + self.deltaBall[1] * i) >= 400):
                        block = i
                        break
            
            # print(self.deltaBall[0])
            if(self.deltaBall[0]>=0):
                # print("right")
                flag = 1
                for i in range(0, block+1):
                    temp = destinationX + flag * self.deltaBall[0]
                    destinationY = destinationY + self.deltaBall[1]
                    if(temp > 200):
                        destinationX = 200
                        flag = flag * -1
                        
                    elif(temp < 0):
                        destinationX = 0
                        flag = flag * -1

                    elif(self.coll(scene_info, temp, destinationY) != -999):
                        destinationX = self.coll(scene_info, temp, destinationY)
                        flag = flag * -1
                        
                    else:
                        destinationX = temp
            else:
                # print("left")
                flag = 1
                for i in range(0, block+1):
                    temp = destinationX + flag * self.deltaBall[0]
                    destinationY = destinationY + self.deltaBall[1]
                    if(temp > 200):
                        destinationX = 200
                        flag = flag * -1
                        
                    elif(temp < 0):
                        destinationX = 0
                        flag = flag * -1

                    elif(self.coll(scene_info, temp, destinationY) != -999):
                        destinationX = self.coll(scene_info, temp, destinationY)
                        flag = flag * -1
                        
                    else:
                        destinationX = temp

            #if(self.coll(scene_info, scene_info['ball'][0] + self.deltaBall[0],  scene_info['ball'][1] + self.deltaBall[1]) != -999):
                #print(self.coll(scene_info, scene_info['ball'][0] + self.deltaBall[0],  scene_info['ball'][0] + self.deltaBall[1]))
                #print(scene_info['ball'])
                
                    

            #print("pre:{}, ball:{}, block:{}".format(destinationX, scene_info['ball'][0], block))
            if(abs((scene_info['platform'][0] + 20) - destinationX) < random.randint(9, 11)):
                command = "NONE"
            elif(scene_info['platform'][0]+20 > destinationX):
                command = "MOVE_LEFT"
            else:
                command = "MOVE_RIGHT"

            if(self.deltaBall[1] < 0):
                if(abs((scene_info['platform'][0] + 20) - scene_info['ball'][0]) < random.randint(9, 11)):
                    command = "NONE"
                elif(scene_info['platform'][0]+20 > scene_info['ball'][0]):
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
