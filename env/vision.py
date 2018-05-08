import tkinter as tk
from time import sleep
import numpy as np


UNIT = 18   # pixels
EXPAND = [(0,-1),(1,0),(0,1),(-1,0)]

class Vision(tk.Tk, object):
    def __init__(self):
        super(Vision, self).__init__()
        self._MapData = []
        self.parkingdict = dict()
        self.robotdict = dict()

        self.resizable(width=False, height=True)


    def initwindows(self, mapfile = "map.txt"):
        map = open(mapfile,'r')

        while 1:
            linestr = map.readline()
            if linestr == "":
                break
            else:
                self._MapData.append(list(linestr.split()))
        self.Height = len(self._MapData)
        self.Width = len(self._MapData[0])

        self.geometry('{0}x{1}'.format((self.Width) * UNIT, (self.Height) * UNIT))
        self.plotform = tk.Canvas(self, height=(self.Height) * UNIT, width=(self.Width) * UNIT, bg='#888888888')

        self._initparkings()

    def _initparkings(self):

        for i in range(self.Height):
            for j in range(self.Width):
                if self._MapData[i][j] == 'P':
                    self.parkingdict[(j,i)] = self.plotform.create_rectangle(j * UNIT, i * UNIT, (j+1)*UNIT, (i+1)*UNIT, fill='white')
                elif self._MapData[i][j] == 'B':
                    self.plotform.create_rectangle(j * UNIT, i * UNIT, (j+1)*UNIT, (i+1)*UNIT, fill='black')
                elif self._MapData[i][j] == 'I':
                    self.plotform.create_rectangle(j * UNIT, i * UNIT, (j+1)*UNIT, (i+1)*UNIT, fill = 'yellow')
                    self.imports = (j, i)
                elif self._MapData[i][j] == 'E':
                    self.plotform.create_rectangle(j * UNIT, i * UNIT, (j+1)*UNIT, (i+1)*UNIT, fill = 'green')
                    self.exit = (j, i)

        self.plotform.pack()

    def setparking(self, pos, havecar = 0):
        if havecar:
            color = 'blue'
        else:
            color = 'white'
        self.plotform.itemconfig(self.parkingdict[pos],fill = color)

    def initrobot(self,robotnu=5):
        for i in range(robotnu):
            self.robotdict[i] = self.plotform.create_rectangle(self.imports[0]*UNIT+UNIT/6,self.imports[1]*UNIT+UNIT/6,
                                             self.imports[0]*UNIT+UNIT*5/6,self.imports[1]*UNIT+UNIT*5/6,fill = 'yellow')
        self.plotform.pack()

    def setrobot(self, robotname, robotstate):
        if robotstate == 0:
            color = 'yellow'
        elif robotstate == 1:
            color = 'blue'
        elif robotstate == 2:
            color = 'green'
        else:
            color = 'red'

        self.plotform.itemconfig(self.robotdict[robotname],fill = color)

    def moverobot(self,robotname, step):
        self.plotform.move(self.robotdict[robotname], *(step*UNIT))

    def astar(self,spos,gpos):

        temp = self._MapData[gpos[1]][gpos[0]]
        self._MapData[gpos[1]][gpos[0]] = 'X'
        openlist = dict()
        closelist = dict()

        openlist[spos] = [(0,0),spos,np.inf,0]

        while not self._expend(openlist,closelist,gpos) and len(openlist):
            pass

        node = gpos
        path = []
        path.append(gpos)
        while 1:
            try:
                node = closelist[node]
                if node == spos:
                    break
                path.append(node)
            except:
                pass
        path.reverse()

        self._MapData[gpos[1]][gpos[0]] = temp
        return path

    def _expend(self,openlist,closelist,gpos):
        node = sorted(openlist.values(),key= lambda x: x[2],reverse= True).pop()
        openlist.pop(node[1])
        if node[1] == gpos:
            closelist[gpos] = node[0]
            return 1
        for i in range(4):
            tempnode = np.array(node[1]) + np.array(EXPAND[i])
            try:
                closelist[tuple(tempnode)]
            except:
                try:
                    if self._MapData[tempnode[1]][tempnode[0]] == 'X':
                        g = node[-1]+1
                        heuris = abs(tempnode[0]-gpos[0]) + abs(tempnode[1]-gpos[1])

                        try:
                            existnode = openlist[tuple(tempnode)]
                            if heuris + g < existnode[2]:
                                openlist[tuple(tempnode)][2] = heuris + g
                        except:
                            nextnode = [node[1], tuple(tempnode), heuris + g, g]
                            openlist[tuple(tempnode)] = nextnode
                except:
                    pass
        closelist[node[1]] = node[0]
        return 0


    def updatesim(self, time=0.1):
        self.update()
        sleep(time)

    def getstate(self):
        print("MapSize:{}x{}, Parking Number:{}".format(self.Height, self.Width, len(self.parkingdict)))



if __name__ == '__main__':

    from env.robot import Robot

    vision = Vision()
    vision.initwindows()
    vision.initrobot(2)
    vision.setrobot(1, 1)


    path = vision.astar(vision.imports, (0, 12))
    robot = Robot(0,vision.imports)
    robot.setpath(path)


    while not robot.IsArrive:
        step = robot.move()
        if tuple(step) == (0,0):
            break
        vision.moverobot(1,step)

        vision.updatesim(0.5)

    stop = input('stop Y/n : ')
    if stop == 'y':
        vision.destroy()

    vision.mainloop()

