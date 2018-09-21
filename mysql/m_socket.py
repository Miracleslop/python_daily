from socket import *


class MSocket(object):
    def __init__(self, aim_address: (), port=-1):
        self.__sock = socket(AF_INET, SOCK_DGRAM)
        t_host = gethostbyname(gethostname())
        if port == -1:
            t_port = 24567
            #   采用UDP
            try:
                #   绑定自身地址
                self.__sock.bind((t_host, t_port))
            except Exception as e:
                t_port += 1
                if t_port > 66666:
                    raise e
            #   绑定的接受数据地址端口
            self.__port = t_port
        else:
            #   绑定自身地址
            self.__sock.bind((t_host, port))
            #   绑定的接受数据地址端口
            self.__port = port

        #   设置目标地址
        self.__aim_address = aim_address

    @property
    def port(self):
        return self.__port

    @property
    def aim_address(self):
        return self.__aim_address

    @aim_address.setter
    def aim_address(self, aim_address: ()):
        self.__aim_address = aim_address

    def sendto(self, msg: str, aim_address=None):
        if aim_address is None:
            self.__sock.sendto(msg.encode('utf8'), self.__aim_address)
        else:
            self.__sock.sendto(msg.encode('utf8'), aim_address)

    def receive(self, seconds=50):
        self.__sock.settimeout(seconds)
        src_byte, src_address = self.__sock.recvfrom(6144)
        return src_byte.decode('utf8'), src_address

    def close(self):
        self.__sock.close()


if __name__ == '__main__':
    print(gethostname())
    print(gethostbyname(gethostname()))
    ms = MSocket(('127.0.1.1', 48964), 48964)
    ms.sendto('send1')
    data, address = ms.receive(5)
    print('%s, %s' % (data, address))
    ret = '456123,456'.split(',')
    print(int(ret[0]))
    print(int(ret[1]))
