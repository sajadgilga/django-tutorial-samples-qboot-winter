from threading import Thread, Lock
from time import sleep

cnt = 0

l = Lock()

def operation(val):
    global cnt
    for i in range(val):
        l.acquire()
        temp = cnt
        sleep(0.0002)
        temp += 10 + val
        cnt = temp
        l.release()


ts = [Thread(target=operation, args=(i,)) for i in range(60)]
[t.start() for t in ts]
[t.join() for t in ts]

print('count is:', cnt)
