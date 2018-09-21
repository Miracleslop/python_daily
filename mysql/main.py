import pymysql.connections
from commun.logger.clog import *
from threading import Thread
from time import sleep
from mysql.m_socket import MSocket

lg = Logger('mysql')


class UpdateSql(object):
    """
    记录更新用的sql
    """

    def __init__(self, select_sql: str, update_sql: str, count_sql: str):
        self.select = select_sql
        self.update = update_sql
        self.count_sql = count_sql


class UpdateTable(object):
    """
    实施更新操作
    """

    class O2N(object):
        """
        存储新老数据，以老数据为key，新数据为value，且key不能重复
        """

        def __init__(self):
            self.__map = {}

        def get(self, key):
            return self.__map[str(key)]

        def put(self, key, value):
            self.__map[str(key)] = str(value)

    def __init__(self, cs):
        self.__cs = cs
        self.__o2n = UpdateTable.O2N()

    def handle_sku(self, begin, end):
        global count
        #   记录失败的返回值
        fr = []
        sql = 'update gc_goods_sku set tgsku_id =  %s where gsku_id = %s'
        #   从SKU表中获取记录，并插入新的ID到tsku_id字段中
        self.__cs.execute('SELECT gsku_id, gspu_id, tgsku_id FROM gc_goods_sku LIMIT %d, %d ' % (begin, end))
        t_value = self.__cs.fetchall()
        lg.info('begin: %d   --  end: %d   --   size: %d ' % (begin, begin + end, t_value.__len__()))
        for i, val in enumerate(t_value):
            index = begin + i + 1
            ret = self.__cs.execute(sql, (str(index), str(val[0])))
            #   根据执行结果 记录日志、显示进度
            if ret != 1 and val[2] is None:
                lg.war('query val:  %s;     index: %d;     --ret: %d' % (val.__str__(), index, ret))
                fr.append(val)
            else:
                count = index
        return fr

    def handle(self, begin, end, update_sql, select_sql):
        global count
        self.__cs.execute(select_sql % (begin, end))
        t_value = self.__cs.fetchall()
        lg.info('begin: %d   --  end: %d   --   size: %d ' % (begin, begin + end, t_value.__len__()))
        for i, val in enumerate(t_value):
            index = begin + i + 1
            try:
                ret = self.__cs.execute(update_sql, (self.__o2n.get(str(val[1])), str(val[0])))
                #   根据执行结果 记录日志、显示进度
                if ret != 1:
                    lg.war('query val:  %s;     index: %d;     --ret: %d' % (val.__str__(), index, ret))
                else:
                    count = index
            except Exception as e:
                #   异常发生时记录数据，跳过 并继续
                lg.error(
                    'query_sql: %s;     query val:  %s;     index: %d;     --Exception: %s' % (
                        select_sql, val.__str__(), index, e.__str__()))

    def init_o2n(self):
        self.__cs.execute('SELECT gsku_id, gspu_id, tgsku_id FROM gc_goods_sku')
        values = cursor.fetchall()
        for val in values:
            self.__o2n.put(val[0], val[2])


#   标记变量用于结束线程，True持续线程，False关闭线程
flag = True
#   记录执行成功的数量
count = 0


def monitor(need_len):
    """
    监控行为，监控的变量count
    :return:
    """
    global count, flag
    try:
        while flag:
            lg.debug("schedule: %d / %d " % (count, need_len))
            sleep(1)
    except Exception as e:
        lg.error('monitor exit AND Exception : %s ' % e.__str__())


def update_handle(cs, cn, sql: UpdateSql, ut: UpdateTable):
    """
    执行sql，并调用监控查看执行情况
    """
    global flag, count
    flag = True
    count = 0
    try:
        #   启动监控线程
        # cs.execute(sql.count_sql)
        # max_len = cs.fetchall()[0][0]
        # t = Thread(target=monitor, args=(max_len,))
        # t.start()

        #   分页执行更新操作每次2000，并提交事务
        # for i in range(int(max_len / 2000) + 1):
        #     ut.handle(i * 2000, 2000, sql.update, sql.select)
        #     cn.commit()
        pass
    except Exception as e:
        cn.rollback()
        raise e
    finally:
        #   结束监控线程
        flag = False
        sleep(3)


def update_handle_sku(cs, cn, ut: UpdateTable):
    """
        特殊行为，用于初始化sku并生成新记录
    """
    global flag, count
    flag = True
    count = 0
    try:
        #   启动监控线程
        # cs.execute('SELECT count(1) FROM gc_goods_sku')
        # max_len = cs.fetchall()[0][0]
        # t = Thread(target=monitor, args=(max_len,))
        # t.start()

        #   绑定服务器地址

        #   分页执行更新操作每次2000，并提交事务
        connect_server(cn, ut)
        # for i in range(int(max_len / 2000) + 1):
        #     ut.handle_sku(i * 2000, 2000)
        #     cn.commit()

    except Exception as e:
        cn.rollback()
        raise e
    finally:
        #   结束监控线程
        flag = False
        sleep(3)


def connect_server(cn, ut: UpdateTable):
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
                be = data.split(',')
                ret = ut.handle_sku(int(be[0]), int(be[1]))
                cn.commit()

                #   循环，以保证该任务执行无误在继续
                while data != 'OK':
                    try:
                        #   发送执行结果到服务器
                        print('SEND: task already complete !')
                        sock.sendto('C2:%s' % ret.__str__())
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


if __name__ == '__main__':
    """
    脚本用于改变数据库中的sku_id
    """
    # https://dev.mysql.com/doc/connector-python/en/connector-python-connectargs.html
    #   start connect
    conn = pymysql.connect(
        user='root', password='W5zg@20180716pre',
        database='w5mall_check', host='192.168.1.22', port=3306,
        charset='utf8mb4'
    )
    cursor = conn.cursor()
    exc = UpdateTable(cursor)

    update_handle_sku(cursor, conn, exc)

    # exc.init_o2n()

    spec = UpdateSql('SELECT gspec_id, gsku_id, gspu_id FROM gc_goods_spec LIMIT %d, %d',
                     'UPDATE gc_goods_spec SET gsku_id = %s WHERE gspec_id = %s',
                     'SELECT count(1) FROM gc_goods_spec ')
    shop_cart = UpdateSql('SELECT sc_id, gsku_id, gspu_id FROM gc_shopping_cart LIMIT %d, %d',
                          'UPDATE gc_shopping_cart SET gsku_id = %s WHERE sc_id = %s',
                          'SELECT count(1) FROM gc_shopping_cart ')

    discount = UpdateSql('SELECT id, gsku_id FROM tc_discount_comm LIMIT %d, %d',
                         'UPDATE tc_discount_comm SET gsku_id = %s WHERE id = %s',
                         'SELECT count(1) FROM tc_discount_comm ')
    order_detail = UpdateSql('SELECT od_id, gsku_id, gspu_id FROM tc_order_detail LIMIT %d, %d',
                             'UPDATE tc_order_detail SET gsku_id = %s WHERE od_id = %s',
                             'SELECT count(1) FROM tc_order_detail ')
    rgr = UpdateSql('SELECT id, gsku_id, gspu_id FROM tc_record_goods_rejected LIMIT %d, %d',
                    'UPDATE tc_record_goods_rejected SET gsku_id = %s WHERE id = %s',
                    'SELECT count(1) FROM tc_record_goods_rejected ')

    srad = UpdateSql('SELECT srd_id, sku_id FROM tc_supplier_return_account_detail LIMIT %d, %d',
                     'UPDATE tc_supplier_return_account_detail SET sku_id = %s WHERE srd_id = %s',
                     'SELECT count(1) FROM tc_supplier_return_account_detail ')
    scag = UpdateSql('SELECT scag_id, gsku_id, gspu_id FROM uc_message_sc_ag LIMIT %d, %d',
                     'UPDATE uc_message_sc_ag SET gsku_id = %s WHERE scag_id = %s',
                     'SELECT count(1) FROM uc_message_sc_ag ')
    # lg.info('-----------update spec-----------')
    # update_handle(cursor, conn, spec, exc)
    # lg.info('-----------update shop_cart-----------')
    # update_handle(cursor, conn, shop_cart, exc)
    # lg.info('-----------update discount-----------')
    # update_handle(cursor, conn, discount, exc)
    # lg.info('-----------update order_detail-----------')
    # update_handle(cursor, conn, order_detail, exc)
    # lg.info('-----------update rgr-----------')
    # update_handle(cursor, conn, rgr, exc)
    # lg.info('-----------update srad-----------')
    # update_handle(cursor, conn, srad, exc)
    # lg.info('-----------update scag-----------')
    # update_handle(cursor, conn, scag, exc)

    cursor.close()
    conn.close()
