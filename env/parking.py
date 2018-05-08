class Parking():
    """single parking property"""
    def __init__(self,pos):
        self.pos = pos
        self.dis = 0
        self.havecar = 0 # is car in there
        self.lefttime = 0
        self.callrobot = 0
        self.couldmove = 0
        self.haverobot = 0
        self.res = 0
        self.path_in = None
        self.path_out = None

    def set_time(self, time):
        self.lefttime = time + 1
        self.havecar = 1
        self.callrobot = 0
        self.couldmove = 0

    def get_time(self,pretime = 40):
        if self.havecar:
            self.lefttime -= 1
            if self.lefttime <= pretime and not self.res:
                self.callrobot = 1
            elif self.lefttime <= 0:
                self.couldmove = 1
        else:
            self.lefttime = 0
        return self.lefttime

    def pickcar(self):
        self.couldmove = 0
        self.havecar = 0
        self.haverobot = 0

    def responce(self):
        self.callrobot = 0
        self.res = 1

    def setpath(self, pathin, pathout):
        self.path_in = pathin
        self.path_out = pathout
        self.dis = len(self.path_out) + len(self.path_in)
        # print("set path successful")

    def reset(self):
        self.havecar = 0  # is car in there
        self.lefttime = 0
        self.callrobot = 0
        self.couldmove = 0
        self.haverobot = 0
        self.res = 0

    def getstate(self,display = False):
        respection = "Parking ({:2},{:2}) have {} car, rest time is {}, callrobot: {}, couldmove: {}".\
            format(self.pos[0],self.pos[1],self.havecar,self.lefttime, self.callrobot, self.couldmove)
        if display:
            print(respection)
        return respection

if __name__ == '__main__':
    parking = Parking((0,0))
    parking.set_time(100)
    parking.getstate(True)