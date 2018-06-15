import os
import logging
# import datetime
import time

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')
LOG = logging.getLogger()


def log(func):
    def wrapper(*args, **kw):
        # LOG.debug('\033[4m')
        LOG.debug('........ begin %s() ! ' % func.__qualname__)
        start = time.time()
        # start = datetime.datetime.now()
        ret = func(*args, **kw)
        end = time.time()
        # end = datetime.datetime.now()
        LOG.debug('........ end %s() !  ps: run time is %.3f ms' % (func.__qualname__, (end - start) * 1000))
        return ret

    return wrapper


class FileRole(object):
    __slots__ = ('__input_path', '__output_path', '__input_data', '__output_data')

    # i_path is __input_path
    # o_path is __output_path
    @log
    def __init__(self, i_path, o_path):
        root_path = os.path.abspath('.')
        root_path = root_path[:root_path.rfind('/')]
        self.__input_path = os.path.join(root_path, i_path)
        LOG.debug('FileRole.__input_path = ' + self.__input_path)
        self.__output_path = os.path.join(root_path, o_path)
        LOG.debug('FileRole.__output_path = ' + self.__output_path)
        self.__input_data = []
        self.__output_data = []

    # read file and store input_data
    # regex is param of split
    @log
    def read(self, regex):

        #   path is file's path
        #   read a path and add a list to __input_data
        def read_data(path):
            with open(path, 'r') as f:
                temp_line = []
                for line in f.readlines():
                    temp = []
                    for col in line.split(regex):
                        temp.append(col.strip())
                    temp_line.append(temp)
                self.__input_data.append(temp_line)

        if os.path.isfile(self.__input_path):
            LOG.debug('start read file:  ' + self.__input_path)
            read_data(self.__input_path)
            LOG.debug('end read file, file name: %s ' % self.__input_path[self.__input_path.rfind('/'):])
        elif os.path.isdir(self.__input_path):
            LOG.debug('start read dir:  ' + self.__input_path)
            for x in os.listdir(self.__input_path):
                t = 'input'
                if x.find(t) != -1:
                    read_data(os.path.join(self.__input_path, x))

                    LOG.debug('end read file, file_name: %s,  read_data_row: %d ' % (
                        x, len(self.__input_data[len(self.__input_data) - 1])))
        else:
            raise IOError('read error in path : \'' + self.__input_path + '\'')

    # convert input_data to output_data
    # f is function
    @log
    def __convert(self, *fun):
        for f in fun:
            LOG.debug('input_data_type: %s,  fun: %s' % (type(self.__input_data), f))
            self.__output_data.append(f(self.__input_data))

    # write data to output_data
    # sign: 1 2 3 4 5
    # r     以只读方式打开文件。文件的指针将会放在文件的开头。这是默认模式。
    # rb    以二进制格式打开一个文件用于只读。文件指针将会放在文件的开头。这是默认模式。
    # r+    打开一个文件用于读写。文件指针将会放在文件的开头。
    # rb+   以二进制格式打开一个文件用于读写。文件指针将会放在文件的开头。
    # w     打开一个文件只用于写入。如果该文件已存在则将其覆盖。如果该文件不存在，创建新文件。
    # wb    以二进制格式打开一个文件只用于写入。如果该文件已存在则将其覆盖。如果该文件不存在，创建新文件。
    # w+    打开一个文件用于读写。如果该文件已存在则将其覆盖。如果该文件不存在，创建新文件。
    # wb+   以二进制格式打开一个文件用于读写。如果该文件已存在则将其覆盖。如果该文件不存在，创建新文件。
    # a     打开一个文件用于追加。如果该文件已存在，文件指针将会放在文件的结尾。也就是说，新的内容将会被写入到已有内容之后。如果该文件不存在，创建新文件进行写入。
    # ab    以二进制格式打开一个文件用于追加。如果该文件已存在，文件指针将会放在文件的结尾。也就是说，新的内容将会被写入到已有内容之后。如果该文件不存在，创建新文件进行写入。
    # a+    打开一个文件用于读写。如果该文件已存在，文件指针将会放在文件的结尾。文件打开时会是追加模式。如果该文件不存在，创建新文件用于读写。
    # ab+   以二进制格式打开一个文件用于追加。如果该文件已存在，文件指针将会放在文件的结尾。如果该文件不存在，创建新文件用于读写。
    @log
    def write(self, *fun):

        """the param must is *fun and is not fun !!! """
        #   self.__convert(fun)
        self.__convert(*fun)

        #   path is file's path
        #   open file's path and write a list in __output_data
        def write_data(path, out_list):
            with open(path, 'w') as f:
                for row in out_list:
                    for cell in row:
                        f.write('%s\t' % cell)
                    f.write('\n')

        if os.path.isfile(self.__output_path):
            LOG.debug('start write file:  ' + self.__output_path)
            write_data(self.__output_path, self.__output_data)
            LOG.debug('end write file: %d ' % len(self.__output_data))
        elif os.path.isdir(self.__output_path):
            LOG.debug('start write dir:  ' + self.__output_path)
            for index, outlist in enumerate(self.__output_data):
                file_name = 'output_' + (index + 1).__str__() + '.txt'
                write_data(os.path.join(self.__output_path, file_name), outlist)
                LOG.debug('end write file, file_name: %s, data_rows: %d' % (file_name, len(outlist)))
        else:
            raise IOError('write error in path : \'' + self.__output_path + '\'')
