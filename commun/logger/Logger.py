__all__ = ['Logger', 'log']

import logging
import os
import time
import sys
import configparser

import ctypes

FOREGROUND_WHITE = 0x0007
FOREGROUND_BLUE = 0x01  # text color contains blue.
FOREGROUND_GREEN = 0x02  # text color contains green.
FOREGROUND_RED = 0x04  # text color contains red.
FOREGROUND_YELLOW = FOREGROUND_RED | FOREGROUND_GREEN

STD_OUTPUT_HANDLE = -11

# std_out_handle = ctypes.oledll.kernel32.GetStdHandle(STD_OUTPUT_HANDLE)
std_out_handle = None


def set_color(color, handle=std_out_handle):
    # bool = ctypes.windll.kernel32.SetConsoleTextAttribute(handle, color)
    # return bool
    pass


# logging.basicConfig(level=logging.DEBUG,
#                     format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')
# logging.basicConfig(level=logging.DEBUG,
#                     format='[%(asctime)s] [%(levelname)s] %(message)s', '%Y-%m-%d %H:%M:%S')
# LOG = logging.getLogger()

config = configparser.ConfigParser()
config.read('/home/l/PycharmProjects/daily-strutil/logger/log_config.ini')


class Logger(object):
    def __init__(self, name, level=logging.DEBUG,
                 file_path='/home/l/PycharmProjects/daily-strutil/docs/tempLog.txt'):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)
        # fmt = logging.Formatter('[%(asctime)s] [%(levelname)s] %(message)s', '%Y-%m-%d %H:%M:%S')
        fmt = logging.Formatter('[%(asctime)s] - [%(name)s] - %(levelname)s - %(message)s', '%Y-%m-%d %H:%M:%S')

        # 设置CMD日志
        sh = logging.StreamHandler()
        sh.setFormatter(fmt)
        sh.setLevel(level)

        # 设置文件日志
        fh = logging.FileHandler(file_path)
        fh.setFormatter(fmt)
        fh.setLevel(level)
        self.logger.addHandler(sh)
        self.logger.addHandler(fh)

    def debug(self, message):
        self.logger.debug(message)

    def info(self, message):
        self.logger.info(message)

    def war(self, message, color=FOREGROUND_YELLOW):
        set_color(color)
        self.logger.warning(message)
        set_color(FOREGROUND_WHITE)

    def error(self, message, color=FOREGROUND_RED):
        set_color(color)
        self.logger.error(message)
        set_color(FOREGROUND_WHITE)

    def cri(self, message):
        self.logger.critical(message)


def log(msg, lg):
    # 如果这里传入 name 然后声明一个 log 即 Logger(name)，则对每条日志会输出两此
    # 所以这里直接传入 log 的引用 lg
    def decorator(func):
        def wrapper(*args, **kwargs):
            lg.debug('%s begin! ' % func.__qualname__)
            lg.info(msg)
            start_time = time.time()
            result = func(*args, **kwargs)
            end_time = time.time()
            lg.debug('%s end! and run time is %.0f ms ' % (func.__qualname__, (end_time - start_time) * 1000))
            return result

        return wrapper

    return decorator


if __name__ == '__main__':
    eg_log = Logger(__name__)
    eg_log.debug('一个debug信息')
    eg_log.info('一个info信息')
    eg_log.war('一个warning信息')
    eg_log.error('一个error信息')
    eg_log.cri('一个致命critical信息')
