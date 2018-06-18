from time import sleep
import os


#   ****************************************
#   fork 的简单使用

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

#   ***********************************************
#   Process的简单使用

from multiprocessing import Process


def run_proc(name, age, **kwargs):
    for i in range(10):
        print('子进程运行中,name=	%s,age=%d	,pid=%d...' % (name, age, os.getpid()))
        print(kwargs)
        sleep(0.3)


if __name__ == "__main__2":
    p = Process(target=run_proc, args=('test', 18), kwargs={"m": 20})
    print('子进程将要执行')
    p.start()
    sleep(1)
    p.terminate()
    p.join()
    print('子进程已结束')

#   ************************************************************
#   ProcessClass 及join 的简单Demo

import time


def worker(interval, id):
    print('worker_%s, 父进程(%s), 当前进程(%s)' % (id, os.getppid(), os.getpid()))
    t_start = time.time()
    time.sleep(interval)  # 程序将会被挂起interval秒
    t_end = time.time()
    print("worker_%s,执行时间为'%0.2f'秒" % (id, t_end - t_start))


#   继承Process类
class ProcessClass(Process):
    # 因为Process类本身也有__init__方法,这个子类相当于重写了这个方法,
    # 但这样就会带来一个问题,我们并没有完全的初始化一个Process类,所以就不能使用从这个
    # 最好的方法就是将继承类本身传递给Process.__init__方法,完成这些初始化操作
    def __init__(self, interval, id):
        Process.__init__(self)
        self.__interval = interval
        self.__id = id

    def run(self):
        worker(self.__interval, self.__id)


if __name__ == '__main__3':
    print("进程ID：%s" % os.getpid())
    p1 = Process(target=worker, args=(2, 1))
    p2 = ProcessClass(1, 2)
    p1.start()
    p2.start()
    # 同时父进程仍然往下执行,如果p2进程还在执行,将会返回True
    print("p2.is_alive=%s" % p2.is_alive())
    # 输出p1和p2进程的别名和pid
    print("p1.name=%s" % p1.name)
    print("p1.pid=%s" % p1.pid)
    print("p2.name=%s" % p2.name)
    print("p2.pid=%s" % p2.pid)
    # join括号中不携带参数,表示父进程在这个位置要等待p1进程执行完成后,
    # 再继续执行下面的语句,一般用于进程间的数据同步,如果不写这一句,
    # 下面的is_alive判断将会是True,在shell(cmd)里面调用这个程序时
    # 可以完整的看到这个过程,大家可以尝试着将下面的这条语句改成p1.join(1),
    # 因为p2需要2秒以上才可能执行完成,父进程等待1秒很可能不能让p1完全执行完成,
    # 所以下面的print会输出True,即p1仍然在执行
    p1.join(1)
    print("p1.is_alive=%s" % p1.is_alive())

#   ************************************************************
#   进程池Pool

from multiprocessing import Pool
import os, time, random


def worker(msg):
    t_start = time.time()
    print("%s开始执行,进程号为%d" % (msg, os.getpid()))
    # random.random()随机生成0~1之间的浮点数
    time.sleep(random.random() * 2)
    t_stop = time.time()
    print(msg, "执行完毕,耗时%0.2f" % (t_stop - t_start))


if __name__ == '__main__4':
    po = Pool(3)
    for i in range(10):
        po.apply_async(worker, (i,))

    print("----start----")
    po.close()  # 关闭进程池,关闭后po不再接收新的请求
    po.join()  # 等待po中所有子进程执行完成,必须放在close语句之后
    print("-----end-----")

#   ************************************************************
#   Queue 消息队列

from multiprocessing import Queue
import random


class QueueDemo(object):
    def __init__(self, maxNum=3, fun=Queue):
        self.__q = fun(maxNum)

    def put_nowait(self, data):
        if not self.__q.full():
            self.__q.put(data)
        else:
            print('消息队列已满, %s 没有入列' % data)

    def get_nowait(self):
        if not self.__q.empty():
            return self.__q.get()
        else:
            return None

    def put(self, data, block=True, timeout=None):
        self.__q.put(data, block, timeout)

    def get(self, block=True, timeout=None):
        return self.__q.get(block, timeout)

    def size(self):
        return self.__q.qsize()


def product(q, block=True, timeout=None, data=random.randrange(1, 10, 1) / 2):
    while True:
        sleep(random.randint(0, 2))
        q.put(data, block, timeout)
        print("进程%s - 入列: %s" % (os.getpid(), data))


def consume(q, block=True, timeout=None):
    while True:
        sleep(random.randint(0, 2))
        da = q.get(block, timeout)
        print("进程%s - 出列: %s" % (os.getpid(), da))


if __name__ == '__main__5':
    q = QueueDemo()
    p1 = Process(target=product, args=(q, True, 3))
    p2 = Process(target=consume, args=(q, True, 3))
    p1.start()
    p2.start()
    p1.join()
    p2.join()

#   ************************************************************
#   进程池Pool

from multiprocessing import Manager, Pool
import os, time, random

__name__ = '__main__6'
if __name__ == '__main__6':
    fun = Manager().Queue
    q = QueueDemo(3, fun)
    po = Pool(1)
    po.apply_async(product, (q,))
    po.apply_async(consume, (q,))
    po.close()
    po.join()
    print('End')

#   ************************************************************
#   多线程-threading

from threading import Thread, enumerate
from time import sleep, ctime

sign_name = 'Lucy'


def sing():
    #   需要修改全局变量时使用global引入全局变量
    global sign_name
    for i in range(3):
        sign_name += str(random.randint(1, 6))
        print('%s 正在唱歌...%d' % (sign_name, i))
        sleep(random.random() * 2)


def dance():
    for i in range(3):
        print('%s 正在跳舞...%d' % (sign_name, i))
        sleep(random.random() * 2)


def show_thread_len():
    while True:
        length = len(enumerate())
        print('当前运行的线程数为:%d' % length)
        if length <= 2:
            break
        sleep(0.5)


if __name__ == '__main__7':
    print('---开始---: %s' % ctime())

    t1 = Thread(target=sing, args=())
    t2 = Thread(target=dance, args=())
    t3 = Thread(target=show_thread_len, args=())

    t1.start()
    t2.start()
    t3.start()

    t1.join()
    t2.join()
    # sleep(5)
    print('---结束---: %s' % ctime())

#   ************************************************************
#   锁Lock类

from threading import *

g_num = 0


def test1():
    global g_num
    for i in range(1000000):
        mutex_flag = mutex.acquire(True)
        if mutex_flag:
            g_num += 1
        mutex.release()
    print('---test1---g_num=%d' % g_num)


def test2():
    global g_num
    for i in range(1000000):
        mutex_flag = mutex.acquire(True)
        if mutex_flag:
            g_num += 1
        mutex.release()
    print("---test2---g_num=%d" % g_num)


if __name__ == '__main__':
    mutex = Lock()

    p1 = Thread(target=test1)
    p1.start()

    p2 = Thread(target=test2)
    p2.start()

    p1.join()

    print('---g_num=%d---' % g_num)
