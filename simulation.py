from env.model import Model
from collections import deque

model = Model(8)
mission = [(68, 100), (78, 150), (23, 100), (69, 100), (79, 150), (29, 100), (65, 100), (75, 150), (25, 100), (59, 100),
           (89, 150), (49, 100)]
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