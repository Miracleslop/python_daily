from commun.logger.clog import Logger
from mysql.m_socket import MSocket
from pymysql import connect

lg = Logger('server')


class Task(object):
    def __init__(self, per: int, total: int):
        """

        :param per: 每个任务需要执行的行数
        :param total: 总行数
        """
        self.__per = per
        self.__total = total
        #   当前任务索引
        self.__index = 0
        #   任务数量
        self.__num = int(self.__total / self.__per)

    def data(self):
        return self.__index * self.__per, self.__per

    def has_next(self):
        return self.__index < self.__num

    def next(self):
        self.__index += 1


class ClientRecord(object):
    def __init__(self, predict_num=0):
        """

        :param predict_num: 预测的客户端数量
        """
        self.__record = {}
        self.__num = predict_num

    def remember(self, client_address):
        self.__record[client_address.__str__()] = 1

    def over(self, client_address):
        self.__record[client_address.__str__()] = 0

    def is_alive(self, client_address):
        return self.__record[client_address.__str__()] == 1

    def is_all_over(self):
        bl = 0
        #   结束的客户端任务数量一定要大于预测的客户端数量
        for k in self.__record:
            if self.__record[k] == 0:
                bl += 1
        return bl >= self.__num

    @property
    def client(self):
        return self.__record.keys()


def server(max_len):
    sock = MSocket((), 8081)

    task = Task(2000, max_len)

    cr = ClientRecord(1)

    while True:
        try:
            data, client_address = sock.receive()
            #   设置目标客户端地址
            sock.aim_address = client_address
            cr.remember(client_address)

            if data.startswith('N2'):
                if task.has_next():
                    #   发送需要执行的任务
                    lg.debug('SEND TASK: aim_address = %s   %s' % (
                        client_address, task.data()))
                    sock.sendto('%d,%d' % task.data())
                    task.next()
                else:
                    #   任务结束，发送结束命令
                    sock.sendto('OVER')
                    lg.debug('SEND OVER: aim_address = %s' % (client_address,))
                    cr.over(client_address)

                    #   如何任务都结束了，就拜拜
                    if cr.is_all_over():
                        break
            elif data.startswith('C2'):
                #   存储结果data
                # 这里注意%后面接的是一个turple，这样会报参数不匹配的错误lg.debug('    SEND OK: aim_address = %s' % client_address)
                lg.debug('    SEND OK: aim_address = %s' % (client_address,))
                sock.sendto('OK')
        except Exception as e:
            lg.debug(e.__str__())
    sock.close()


if __name__ == '__main__':
    conn = connect(
        user='root', password='W5zg@20180716pre',
        database='w5mall_check', host='192.168.1.22', port=3306,
        charset='utf8mb4'
    )
    cursor = conn.cursor()
    cursor.execute('SELECT count(1) FROM gc_goods_sku')
    max_len = cursor.fetchall()[0][0]
    server(max_len)

    cursor.close()
    conn.close()
    pass
