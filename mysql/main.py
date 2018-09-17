import mysql.connector
from commun.logger.clog import *

lg = Logger('mysql')

QUERY_sku = 'SELECT gsku_id, gspu_id, ttgsku_id FROM gc_goods_sku ORDER BY gsku_id'
QUERY_spec = 'SELECT gspec_id, gsku_id, gspu_id FROM gc_goods_spec ORDER BY gsku_id'
QUERY_shop_cart = 'SELECT sc_id, gsku_id, gspu_id FROM gc_shopping_cart ORDER BY gsku_id'
QUERY_discount = 'SELECT id, gsku_id FROM tc_discount_comm ORDER BY gsku_id'
QUERY_od = 'SELECT od_id, gsku_id, gspu_id FROM tc_order_detail ORDER BY gsku_id'
QUERY_rgr = 'SELECT id, gsku_id, gspu_id FROM tc_record_goods_rejected ORDER BY gsku_id'
QUERY_srad = 'SELECT srd_id, sku_id FROM tc_supplier_return_account_detail ORDER BY sku_id'
QUERY_scag = 'SELECT scag_id, gsku_id, gspu_id FROM uc_message_sc_ag ORDER BY gsku_id'

o2n = {}


def handle_spec(cs):
    #   convert spec
    #   Id skuId spuId
    cs.execute(QUERY_spec)
    values = cs.fetchall()
    for val in values:
        if str(val[1]) in o2n:
            cs.execute('UPDATE gc_goods_spec SET gsku_id = %s WHERE gspec_id = %s AND gsku_id = %s AND gspu_id = %s' % (
                o2n[str(val[1])], str(val[0]), str(val[1]), str(val[2])))
            # lg.debug('update gc_goods_spec %s  skuId to %s, and ret = %s' % (str(val), o2n[str(val[1])], cs.rowcount))
        else:
            lg.debug('update gc_goods_spec %s skuId is not exist !' % str(val))


def handle_shop_cart(cs):
    #   convert gc_shopping_cart
    #   sc_id, gsku_id, gspu_id
    cs.execute(QUERY_shop_cart)
    values = cs.fetchall()
    for val in values:
        if str(val[1]) in o2n:
            cs.execute('UPDATE gc_shopping_cart SET gsku_id = %s WHERE sc_id = %s AND gsku_id = %s AND gspu_id = %s' % (
                o2n[str(val[1])], str(val[0]), str(val[1]), str(val[2])))
            # lg.debug(
            #     'update gc_shopping_cart %s  skuId to %s, and ret = %s' % (str(val), o2n[str(val[1])], cs.rowcount))
        else:
            lg.debug('update gc_shopping_cart %s skuId is not exist !' % str(val))


def handle_discount(cs):
    #   convert tc_discount_comm
    #   id, gsku_id
    cs.execute(QUERY_discount)
    values = cs.fetchall()
    for val in values:
        if str(val[1]) in o2n:
            cs.execute('UPDATE tc_discount_comm SET gsku_id = %s WHERE id = %s AND gsku_id = %s' % (
                o2n[str(val[1])], str(val[0]), str(val[1])))
            # lg.debug(
            #     'update tc_discount_comm %s  skuId to %s, and ret = %s' % (str(val), o2n[str(val[1])], cs.rowcount))
        else:
            lg.debug('update tc_discount_comm %s skuId is not exist !' % str(val))


def handle_od(cs):
    #   convert tc_order_detail
    #   od_id, gsku_id, gspu_id
    cs.execute(QUERY_od)
    values = cs.fetchall()
    for val in values:
        if str(val[1]) in o2n:
            cs.execute('UPDATE tc_order_detail SET gsku_id = %s WHERE od_id = %s AND gsku_id = %s AND gspu_id = %s' % (
                o2n[str(val[1])], str(val[0]), str(val[1]), str(val[2])))
            # lg.debug('update tc_order_detail %s  skuId to %s, and ret = %s' % (str(val), o2n[str(val[1])], cs.rowcount))
        else:
            lg.debug('update tc_order_detail %s skuId is not exist !' % str(val))


def handle_rgr(cs):
    #   convert tc_record_goods_rejected
    #   id, gsku_id, gspu_id
    cs.execute(QUERY_rgr)
    values = cs.fetchall()
    for val in values:
        if str(val[1]) in o2n:
            cs.execute(
                'UPDATE tc_record_goods_rejected SET gsku_id = %s WHERE id = %s AND gsku_id = %s AND gspu_id = %s' % (
                    o2n[str(val[1])], str(val[0]), str(val[1]), str(val[2])))
            # lg.debug('update tc_record_goods_rejected %s  skuId to %s, and ret = %s' % (
            #     str(val), o2n[str(val[1])], cs.rowcount))
        else:
            lg.debug('update tc_record_goods_rejected %s skuId is not exist !' % str(val))


def handle_srad(cs):
    #   convert tc_supplier_return_account_detail
    #   srd_id, sku_id
    cs.execute(QUERY_srad)
    values = cs.fetchall()
    for val in values:
        if str(val[1]) in o2n:
            cs.execute(
                'UPDATE tc_supplier_return_account_detail SET sku_id = %s WHERE srd_id = %s AND sku_id = %s' % (
                    o2n[str(val[1])], str(val[0]), str(val[1])))
            # lg.debug('update tc_supplier_return_account_detail %s  skuId to %s, and ret = %s' % (
            #     str(val), o2n[str(val[1])], cs.rowcount))
        else:
            lg.debug('update tc_supplier_return_account_detail %s skuId is not exist !' % str(val))


def handle_scag(cs):
    #   convert uc_message_sc_ag
    #   scag_id, gsku_id, gspu_id
    cs.execute(QUERY_scag)
    values = cs.fetchall()
    for val in values:
        if str(val[1]) in o2n:
            cs.execute(
                'UPDATE uc_message_sc_ag SET gsku_id = %s WHERE scag_id = %s AND gsku_id = %s AND gspu_id = %s' % (
                    o2n[str(val[1])], str(val[0]), str(val[1]), str(val[2])))
            lg.debug(
                'update uc_message_sc_ag %s  skuId to %s, and ret = %s' % (str(val), o2n[str(val[1])], cs.rowcount))
        else:
            lg.debug('update uc_message_sc_ag %s skuId is not exist !' % str(val))


def handle_sku(cs):
    #   get old_skuId and new_skuId from sku
    #   skuId spuId
    cs.execute(QUERY_sku)
    values = cs.fetchall()
    o2n = {}
    with open('/home/l/PycharmProjects/daily-strutil/mysql/handleSku', 'w') as f:
        for i, val in enumerate(values):
            o2n[str(val[0])] = str(i + 1)
            # cs.execute('update gc_goods_sku set tgsku_id =  %s where gsku_id = %s' % (str(i + 1), str(val[0])))
            f.write('update gc_goods_sku set tgsku_id =  %s where gsku_id = %s' % (str(i + 1), str(val[0])))
    lg.debug(cs.rowcount)


if __name__ == '__main__':
    # https://dev.mysql.com/doc/connector-python/en/connector-python-connectargs.html

    #   start connect
    conn = mysql.connector.connect(
        user='root', password='root',
        database='w5maltest', host='192.168.2.98', port='3306',
        charset='utf8mb4', collation='utf8mb4_general_ci'
    )
    cursor = conn.cursor()

    #   get old_skuId and new_skuId from sku
    #   skuId spuId
    cursor.execute(QUERY_sku)
    values = cursor.fetchall()
    for i, val in enumerate(values):
        o2n[str(val[2])] = str(val[0])

    #   print(values)
    for k, v in o2n.items():
        lg.debug(k + " : " + v)

    # handle_spec(cursor)
    # handle_shop_cart(cursor)
    # handle_discount(cursor)
    # handle_od(cursor)
    # handle_rgr(cursor)
    # handle_srad(cursor)
    # handle_scag(cursor)

    handle_sku(cursor)

    conn.commit()
    cursor.close()
    conn.close()

sign = -1

#
# def getOld2NewSku(ec: excel):
#     o2n = {}
#
#     def sku_handle(rw: []):
#         if sign == -1:
#             for i, x in enumerate(rw):
#                 if x.count('sku') > 0 and x.count('id') > 0:
#                     sign = i
#                     break
#         else:
#             return [rw[0], rw[sign]]
#
#     ec.handle(1, sku_handle)
#     return o2n
#     pass
#
#
# def convertSku(ec: excel, o2n: {}):
#     pass
#
#
# if __name__ == '__main__':
#     sku = excel('/home/l/文档/gc_goods_sku.xlsx')
#     spec = excel('/home/l/文档/gc_goods_spec.xlsx')
#     shop_cart = excel('/home/l/文档/gc_shopping_cart.xlsx')
#     dit_comm = excel('/home/l/文档/tc_discount_comm.xlsx')
#     od = excel('/home/l/文档/tc_order_detail.xlsx')
#     rgr = excel('/home/l/文档/tc_record_goods_rejected.xlsx')
#     gsi_rad = excel('/home/l/文档/tc_supplier_return_account_detail.xlsx')
#     sc_ag = excel('/home/l/文档/uc_message_sc_ag.xlsx')
#     o2n_sku = getOld2NewSku(sku)
#     convertSku(spec, o2n_sku)
#     pass
