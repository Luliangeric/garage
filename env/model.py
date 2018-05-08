from env.vision import Vision
from env.robot import Robot
from env.parking import Parking

class Model(Vision):
    def __init__(self, robotnum = 5):
        super().__init__()
        self.robotnum = robotnum
        self._initmodel()

        self.t = 0

        self.simustop = 0

        self.EIpath = self.astar(self.exit,self.imports)

        self.printcallinfo = 1
        self.printassigninfo = 1

    def _initmodel(self):
        self.initwindows()
        self.initrobot(self.robotnum)
        self._bindparking()
        self._bindrobot()
        super().getstate()

    def _bindparking(self):
        templist = list()
        self.parkingindex = dict()
        for pos in self.parkingdict.keys():
            temp = Parking(pos)
            temp.setpath(self.astar(self.imports,pos),self.astar(pos,self.exit))
            templist.append(temp)
        templist.sort(key= lambda x : x.dis)
        # print([i.dis for i in iter(templist)])
        for i, p in enumerate(iter(templist)):
            self.parkingindex[i] = p

    def _bindrobot(self):
        self.robotindex = dict()
        self.robot2parking = dict()
        # self.parking2robot = dict()
        for i in self.robotdict.keys():
            robot = Robot(i,self.imports)
            self.robotindex[i] = robot
            self.robot2parking[i] = None

    def action(self, parkingnum, time):
        robotlist = [r for r in self.robotindex.values() if tuple(r.pos) == self.imports and r.state == 0]
        try:
            selerobot = robotlist.pop()
            selerobot.state = 1
            parking = self.parkingindex[parkingnum]
            parking.set_time(time)
            selerobot.setpath(parking.path_in)

            self.setrobot(selerobot.name, selerobot.state)
            self.robot2parking[selerobot.name] = parkingnum
            self.printassigninfo = 1
            return True
        except:
            if self.printassigninfo:
                print(str(self.t) + ":All robots are busy, {} Assign is failed!".format(parkingnum))
                self.printassigninfo = 0
            return False


    def state(self):

        pass

    def step(self, timestep = 0.1):
        for key, parking in self.parkingindex.items():
            parking.get_time()
            # if parking.havecar:
            #     parking.getstate(True)
            if parking.callrobot:
                robotlist = [r for r in self.robotindex.values() if r.state == 0]
                robotlist.sort(key=lambda x: abs(x.pos[0] - parking.pos[0]) + abs(x.pos[1] - parking.pos[1]),
                               reverse=True)
                try:
                    selerobot = robotlist.pop()
                    self.robot2parking[selerobot.name] = key

                    selerobot.setpath(self.astar(tuple(selerobot.pos), parking.pos))
                    selerobot.state = 3
                    self.setrobot(selerobot.name, selerobot.state)

                    parking.responce()
                    self.printcallinfo = 1
                except:
                    if self.printcallinfo:
                        print(str(self.t) + ":All robots are busy, {} Calling is failed!".format(key))
                        self.printcallinfo = 0

            if parking.haverobot and parking.couldmove:
                temp = [(rnum, pnum) for rnum, pnum in self.robot2parking.items() if pnum == key]
                self.robot2parking[temp[0][0]] = None
                robot = self.robotindex[temp[0][0]]
                robot.state = 2
                robot.setpath(parking.path_out)
                parking.pickcar()

                self.setrobot(robot.name, robot.state)
                self.setparking(parking.pos, parking.havecar)

        for key, robot in self.robotindex.items():
            # robot.getstate(True)
            if not robot.IsBusy:
                continue
            step = robot.move()
            if robot.IsArrive:
                robot.IsBusy = 0
                if robot.state == 1:
                    robot.state = 0
                    pnum = self.robot2parking[key]
                    self.robot2parking[key] = None
                    parking = self.parkingindex[pnum]
                    path = parking.path_in
                    path.pop()
                    path.reverse()
                    path.append(self.imports)
                    robot.setpath(path)

                    self.setrobot(key,robot.state)
                    self.setparking(parking.pos, parking.havecar)

                if robot.state == 2:
                    robot.state = 0
                    robot.setpath(self.EIpath)

                    self.setrobot(key, robot.state)

                if robot.state == 3:
                    pnum = self.robot2parking[key]
                    parking = self.parkingindex[pnum]
                    parking.haverobot = 1

            self.moverobot(key, step)

        self.updatesim(timestep)
        self.t += 1

        flag = any([r.IsBusy for r in self.robotindex.values()]) \
               or any([p.havecar for p in self.parkingindex.values()])
        self.simustop = not flag

    def reset(self):
        for _, robot in self.robotindex.items():
            robot.reset(self.imports)
        for _, parking in self.parkingindex.items():
            parking.reset()
        self.robot2parking.clear()
        for i in self.robotdict.keys():
            self.robot2parking[i] = None
        print("System reset successfully")
        return 1

    def getinfo(self, dispaly = 'a'):
        if dispaly == 'a' or dispaly == 'p':
            for key, item in self.parkingindex.items():
                if item.havecar:
                    fparking = 'Number:{:3}-'.format(key) + item.getstate() + ' dis: {}'.format(item.dis)
                    print(fparking)
        if dispaly == 'a' or dispaly == 'r':
            for key, item in self.robotindex.items():
                frobot = 'Number:{:2}-'.format(key) + item.getstate()
                print(frobot)
        if dispaly == 'a' or dispaly == 'b':
            for key, item in self.robot2parking.items():
                bindinfo = 'Robot {} is binded with Parking {}'.format(key, item)
                print(bindinfo)

if __name__ == '__main__':
    from collections import deque


    model = Model(8)
    # for i in range(len(model.parkingindex)):
    #     pos = model.parkingindex[i]
    #     model.setparking(pos.pos,1)
    #     model.updatesim(0.002)


    # robot = model.robotindex[0]
    # parking = model.parkingindex[1]
    # robot.setpath(parking.path_in)
    # flag = 1
    # while not robot.IsArrive:
    #     step = robot.move()
    #     if robot.IsArrive:
    #         model.setparking(parking.pos,1)
    #         if flag:
    #             robot.setpath(parking.path_out)
    #             flag = 0
    #     model.moverobot(0, step)
    #     model.updatesim(0.5)
    mission = [(68, 100),(78,150),(23,100),(69, 100),(79,150),(29,100),(65, 100),(75,150),(25,100),(59, 100),(89,150),(49,100)]
    carlist = deque(mission)
    flag = 1
    while not model.simustop:
        while 1:
            try:
                task = carlist.popleft()
                if model.action(*task):
                    pass
                else:
                    carlist.appendleft(task)
                    break
                flag = 1
            except:
                if flag:
                    print("Mission is empty")
                    flag = 0
                break

        model.step(0.2)


    model.destroy()
    model.mainloop()