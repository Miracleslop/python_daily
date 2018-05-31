import os
import logging
from logging import Logger
from typing import Type

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')
LOG = logging.getLogger()


class FileRole(object):
    __slots__ = ('__input_path', '__output_path', '__input_data', '__output_data')

    # i_path is __input_path
    # o_path is __output_path
    def __init__(self, i_path, o_path):
        LOG.debug('FileRole is initting ! ')
        root_path = os.path.abspath('.')
        root_path = root_path[:root_path.rfind('/')]
        self.__input_path = os.path.join(root_path, i_path)
        LOG.debug('FileRole.__input_path = ' + self.__input_path)
        self.__output_path = os.path.join(root_path, o_path)
        LOG.debug('FileRole.__output_path = ' + self.__output_path)
        self.__input_data = []
        self.__output_data = []
        LOG.debug('init complete ! ')
        pass

    # read file and store input_data
    # regex is param of split
    def read(self, regex):
        def read_data(path):
            with open(path) as f:
                for line in f.readlines():
                    temp = []
                    for col in line.split(regex):
                        temp.append(col.strip())
                    self.__input_data.append(temp)

        if os.path.isfile(self.__input_path):
            LOG.debug('start read data of file:  ' + self.__input_path)
            read_data(self.__input_path)
            LOG.debug('end read data of file')
        elif os.path.isdir(self.__input_path):
            LOG.debug('start read data of dir:  ' + self.__input_path)
            for x in os.listdir(self.__input_path):
                t = 'input'
                if x.find(t) != -1:
                    read_data(os.path.join(self.__input_path, x))
                    LOG.debug('end read data of dir, file name: ' + x)
        else:
            raise IOError('read error in path : \'' + self.__input_path + '\'')
        LOG.debug('read data complete')

    # convert input_data to output_data
    # f is function
    def __convert(self, *fun):
        for f in fun:
            self.__output_data.append(f(self.__input_data))

    # write data to output_data
    # sign: 1 2 3 4 5
    def write(self, sign, fun):
        self.__convert(fun)

        def write_data(path, output_data):
            with open(path) as f:
                for 

        if os.path.isfile(self.__output_path):
            LOG.debug('start write data of file:  ' + self.__output_path)
            write_data(self.__output_path, self.__output_data)
            LOG.debug('end write data of file')
        elif os.path.isdir(self.__output_path):
            LOG.debug('start write data of dir:  ' + self.__output_path)
            for x in os.listdir(self.__output_path):
                t = 'output_' + sign
                if x.find(t) != -1:
                    write_data(os.path.join(self.__output_path, x), self.__output_data)
                    LOG.debug('end write data of dir, file name:' + x)
                    break
        else:
            raise IOError('write error in path : \'' + self.__output_path + '\'')
        LOG.debug('wirte data is complete')
