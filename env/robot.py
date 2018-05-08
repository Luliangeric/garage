import numpy as np
class Robot():
    """single robot property"""
    def __init__(self, name, pos):
        self.name = name
        self.pos = np.array(pos)
        self.state = 0 # 0 is free, 1 is carryin ,2 is carryout, 3 is call
        self.IsBusy = 0
        self.IsArrive = 0
        self.path = None

    def move(self):
        try:
            nextpos = np.array(next(self.path))
            step = nextpos - self.pos
            self.pos = nextpos
            return step
        except:
            self.path = None
            self.IsArrive = 1
            return np.array((0, 0))

    def setpath(self,path):
        self.path = iter(path)
        self.IsBusy = 1
        self.IsArrive = 0

    def reset(self,pos):
        self.pos = pos
        self.IsArrive = 0
        self.IsBusy = 0
        self.path = None
        self.state = 0


    def getstate(self,display = False):
        respection = "Robot({}) is at ({:2},{:2}), busy: {}, arrive: {}, state: {}".\
              format(self.name,self.pos[0],self.pos[1],self.IsBusy,self.IsArrive,self.state)
        if display:
            print(respection)
        return respection

if __name__ == '__main__':
    robot = Robot(1,(1,2))
    path = [(2,3),(3,4),(4,5),(5,6)]
    robot.setpath(path)
    while not robot.IsArrive:
        print(robot.move())
        robot.getstate(True)




