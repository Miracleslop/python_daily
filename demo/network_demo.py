# coding=utf-8

from socket import *
from time import *
from threading import Thread, enumerate


# s_tcp = socket(AF_INET, SOCK_STREAM)


def server():
    sendAdder = ('192.168.2.157', 8080)
    s_udp = socket(AF_INET, SOCK_DGRAM)
    try:
        s_udp.bind(sendAdder)
        while True:
            data, addr = s_udp.recvfrom(1024)
            print(data, addr)
    finally:
        s_udp.close()


def clien():
    sendAdder = ('192.168.2.157', 8080)
    num = 0
    s_udp = socket(AF_INET, SOCK_DGRAM)
    try:
        while True:
            sleep(1)
            num += 1
            temp_data = '[%s] - message-%d !!' % (ctime(), num)
            sendData = temp_data.encode()
            s_udp.sendto(sendData, sendAdder)
            print(temp_data)
    finally:
        s_udp.close()


t1 = Thread(target=server, args=())
t2 = Thread(target=clien, args=())

t1.start()
t2.start()
t1.join()
t2.join()
