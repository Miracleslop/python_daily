from commun.logger import clog
from abc import ABCMeta, abstractmethod

lg = clog.Logger("htmlity")


class HtmlTag(object):
    __metaclass__ = ABCMeta

    """
    html tag 类，记录相关信息
    """

    def __init__(self, start_sign: str, end_sign: str):
        """
        初始化并记录一个过滤标签
        :param start_sign: 过滤标签的起始标记
        :param end_sign: 过滤标签的结束标记
        """
        self.__start_sign = start_sign
        self.__end_sign = end_sign
        self.__start_len = len(start_sign)
        self.__end_len = len(end_sign)

    @property
    def start_sign(self):
        return self.__start_sign

    @property
    def end_sign(self):
        return self.__end_sign

    @property
    def start_len(self):
        return self.__start_len

    @property
    def end_len(self):
        return self.__end_len

    @abstractmethod
    def _predicate(self, i, content: str):
        """
        用于判断是否已经读取到标签结束标记，需要在子类中重写该方法用于判断
        :param i:   遍历content起始下标
        :param content: 需要检查的文本内容
        :return:
        """
        pass

    def _opt(self, begin, end, content: str):
        """
        可在子类中重写该方法对被过滤的内容采取不容的措施，不重写则表示略过
        :param begin: 开始标记的后一个字符下标
        :param end: 结束标记的前一个字符的下标
        :param content: 目标的文本内容
        :return:
        """
        pass

    def skip_content(self, i, content: str):
        """
        对从下标i开始的文本content跳到结束标记的后面一个字符，并返回该字符的下标
        一般下标i为开始标记后面一个字符的下标
        :param i:
        :param content:
        :return:
        """
        old_i = i
        while i < len(content):
            step = self._predicate(i, content)
            if step != 0:
                i += step
                self._opt(old_i, i - 1 - self.__end_len, content)
                break
            i += 1
        return i


class HtmlTagStart(HtmlTag):
    """
    继承HtmlTag  结束标记是以<为开始
    """

    def _predicate(self, i, content: str):
        """
        __skip_by_start
        搜寻字符串是以开头的<为标志的
        :param i: 起始位置
        :param content: 要过滤的内容
        :return:
        """
        if content[i] == '<' and content[i:i + self.end_len] == self.end_sign:
            return self.end_len
        else:
            return 0


class HtmlTagEnd(HtmlTag):
    """
    继承HtmlTag 结束标记是以>为开始
    """

    def _predicate(self, i, content: str):
        """
        __skip_by_end
        搜寻字符串是以结尾处>为标志的
        :param i: 起始位置
        :param content: 要过滤的内容
        :return:
        """
        if content[i] == '>' and content[i - self.end_len + 1: i + 1] == self.end_sign:
            return 1
        else:
            return 0
