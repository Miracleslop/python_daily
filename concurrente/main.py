from time import sleep
import os


def sing():
    for i in range(3):
        print('sing~~%d' % i)
        sleep(2)


def dance():
    for i in range(3):
        print('dance~~%d' % i)
        sleep(1)


if __name__ == "__main__1":
    num = 0
    sign = 1
    print('main thread is here--sign: %d' % sign)
    sign += 1
    pid = os.fork()
    if pid == 0:
        sign -= 1  # child thread run
    elif pid > 0:
        sign += 1  # main thread run
    else:
        print('creat fail')
    print('main and child thread both is here--sign: %d' % sign)

    if pid < 0:
        print('fail')
    elif pid == 0:
        num += 1
        print("我是子进程(%s),我的父进程是(%s)----%d" % (os.getpid(), os.getppid(), num))
        dance()
    else:
        num += 1
        print("我是父进程(%s),我的子进程是(%s)----%d" % (os.getpid(), pid, num))
        sing()

from multiprocessing import Process


def run_proc(name, age, **kwargs):
    for i in range(10):
        print('子进程运行中,name=	%s,age=%d	,pid=%d...' % (name, age, os.getpid()))
        print(kwargs)
        sleep(0.3)


if __name__ == "__main__":
    p = Process(target=run_proc, args=('test', 18), kwargs={"m": 20})
    print('子进程将要执行')
    p.start()
    sleep(1)
    p.terminate()
    p.join()
    print('子进程已结束')
