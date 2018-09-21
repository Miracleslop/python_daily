from mysql.m_socket import MSocket
from time import sleep

if __name__ == '__main__':
    #   绑定服务器地址
    sock = MSocket(('127.0.1.1', 8081))

    #   开始接受任务并处理
    try:
        while True:
            sock.sendto('N2%d' % sock.port)
            print('SEND: request next task !')
            try:
                data, server_address = sock.receive(5)
                print('    RECEIVE TASK: data = %s,  from %s' % (data, server_address))
                if data == 'OVER':
                    print('Task OVER')
                    break

                #   执行任务
                sleep(2)
                #   记录结果
                ret = '(123,123,123)'

                #   循环，以保证该任务执行无误在继续
                while data != 'OK':
                    try:
                        #   发送执行结果到服务器
                        print('SEND: task already complete !')
                        sock.sendto('C2:%s' % ret)
                        #   等待100秒接收服务器响应
                        data, server_address = sock.receive()
                        print('    RECEIVE REP: data = %s,  from %s' % (data, server_address))
                    except Exception as ex:
                        print('        EXCEPTION: send task result fail    Exception: %s' % ex.__str__())
                        data = 'NOOK'

            except Exception as e:
                print('        EXCEPTION: receive task fail    Exception: %s' % e.__str__())

    finally:
        sock.close()
