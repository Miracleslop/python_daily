from xlrd import *


class excel(object):
    """
    read excel class
    """
    def __init__(self, wb):
        self.__workbook = open_workbook(wb)

    def sheet(self, i):
        return self.__workbook.sheet_by_index(i)

    def handle(self, i, fun, r=None):
        def th(_rw: []):
            trw = [str(x.value) for x in _rw]
            for x in trw:
                print('%s' % x, end=';')
            for x in fun(trw):
                print('%s' % x, end=';')
            print()

        if not r:
            for rw in self.sheet(i).get_rows():
                th(rw)
        else:
            rw = self.sheet(i).row(r)
            th(rw)


def synom_clear(rw: list):
    """
    handle third cate
    :param rw: a row data
    :return:   content after handle
    """
    nrw = [str(x) for x in rw]
    #   filter 运动,婴童,婴儿,儿童,女士,男士,孕婴
    filter = ['运动', '婴童', '婴儿', '儿童', '女士', '男士', '孕婴', '成人', '母婴']

    #   first filter specil word
    for fl in filter:
        nrw[1] = nrw[1].replace(fl, '')
        nrw[2] = nrw[2].replace(fl, '')

    #   second join 1 and 2, and that must be lowercase
    tstr = nrw[1].lower() + ',' + nrw[2].lower()

    #   third handle key word
    ret = ''
    arr = tstr.split(',')
    for si in range(arr.__len__()):
        bol = False
        for msi in range(si + 1, arr.__len__()):
            if arr[si] == (arr[msi]):
                bol = True
                break
        if not bol:
            ret = ret + arr[si] + ','
    if ret.endswith(','):
        ret = ret[:-1]
    return [nrw[0], nrw[1], ret]


if __name__ == '__main__1':
    ins = excel('/home/l/文档/synom.xlsx')
    ins.handle(2, synom_clear)

ret = ''


def findTable(key):
    pass


if __name__ == '__main__2':
    """
    findTable 
    """
    with open('/home/l/文档/db.sql', 'r') as f:
        isFind = False
        for line in f.readlines():
            if line.startswith('CREATE'):
                ret = ''
                ret += line
                isFind = False
            elif line.startswith(') ENGINE') and isFind:
                ret += line
                print(ret)
                ret = ''
                isFind = False
            elif line.count('sku') > 0:
                ret += line
                isFind = True
            else:
                ret += line

