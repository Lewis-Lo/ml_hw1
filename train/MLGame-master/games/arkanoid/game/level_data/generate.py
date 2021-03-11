import random
import numpy as np

def check(x, y, bricksX, bricksY):
    for i in range(0, len(bricksX)):
        if(x == bricksX[i] and y == bricksY[i]):
            return True
        
    return False


if __name__ == '__main__':
    index = range(6, 21)
    print(str(index[0]) + '.dat')
    print(type(index[0]))
    for i in range(0, 15):
        file = open(str(index[i]) + '.dat', 'w')

        offset = '25 50 -1'
        file.write(offset)

        numOfBricks = random.randint(5, 30)
        bricksX = []
        bricksY = []
        for i in range(0, numOfBricks):
            pos = [0, 0]
            pos[0] = random.randint(0, 6)
            pos[1] = random.randint(0, 4)
            pos[0] = pos[0] * 25
            pos[1] = pos[1] * 25

            if(check(pos[0], pos[1], bricksX, bricksY) == False):
                file.write('\n')
                bricksX.append(pos[0])
                bricksY.append(pos[1])
                file.write("{} {} 0".format(str(pos[0]), str(pos[1])))
            



        file.close()
    
    