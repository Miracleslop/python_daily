from urllib import request
from urllib import parse
from urllib import error
from commun.logger import clog
import io

lg = clog.Logger("web_spider")


class FilterStrategy(object):
    def __init__(self, text: str):
        """
        :param text:  待过滤的文本
        """
        self.__text = text
        self.__len = len(text)
        self.__switch = {
            '<scr': ('<script', '</script>', self.__skip_by_start),
            '<!--': ('<!--', '-->', self.__skip_by_end),
            '<lin': ('<link', '/>', self.__skip_by_end),
            '<cod': ('<code', '</code>', self.__skip_by_start)
        }

    def __skip_by_end(self, i, end_sign):
        end_len = len(end_sign)
        if self.__text[i] == '>' and self.__text[i - end_len + 1: i + 1] == end_sign:
            return 1
        else:
            return 0

    def __skip_by_start(self, i, end_sign):
        end_len = len(end_sign)
        if self.__text[i] == '<' and self.__text[i:i + end_len] == end_sign:
            return end_len
        else:
            return 0

    @clog.log('filter script content ! ', lg)
    def filter(self):

        io_text = io.StringIO()
        old_i = 0
        i = 0
        while i < self.__len:
            if self.__text[i] == '<':
                sel = self.__switch.get(self.__text[i:i + 4])
                if sel is not None:
                    sel_len = len(sel[0])
                    if self.__text[i:i + sel_len] == sel[0]:
                        io_text.write(self.__text[old_i:i])

                        # i调转到<script后面第一个字符的下标
                        i += sel_len

                        #
                        while i < self.__len:
                            step = sel[2](i, sel[1])
                            if step != 0:
                                i += step
                                break
                            i += 1

                        #
                        old_i = i
                        continue
            i += 1

        res_text = io_text.getvalue()
        io_text.close()
        return res_text


@clog.log('downloading...', lg)
def load_page(req_url: str):
    """
    加载页面，爬去返回页面文本并返回
    :param req_url:	请求
    :return: 返回解码后的文本 
    """
    head = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/64.0.3282.140 Safari/537.36 Edge/17.17134 "
    }
    rqs = request.Request(req_url, headers=head)
    rqs.add_header("Connection", "keep-alive")
    rps = request.urlopen(rqs)
    html_byte = rps.read()
    html_str = html_byte.decode('utf-8')
    return html_str


@clog.log('writing...', lg)
def write_file(content: str, path):
    """
    作用：把str写入相应路径的文件
    :param content:需要写入的str
    :param path: 写入文件的路径
    :return:写入结束不返回值
    """
    with open(path, 'w') as f:
        f.write(content)


@clog.log('spidering...', lg)
def tieba_spider(req_url, begin_page, end_page):
    """
    作用：负责处理url，分配每个url去发送请求
    :param req_url: 需要处理的第一个url
    :param begin_page: 爬虫执行的起始页面
    :param end_page: 爬虫执行的截止页面
    :return:
    """

    for page in range(begin_page, end_page + 1):
        pn = (page - 1) * 50

        filename = "page " + str(page) + ".html"
        full_url = '%s&pn=%d' % (req_url, pn)

        html_0x = load_page(full_url)
        fs = FilterStrategy(html_0x)
        html_u8 = str(fs.filter())
        write_file(html_u8, filename)


if __name__ == "__main__":
    kw = "lol"
    beginPage = 1
    endPage = 1
    url = "http://tieba.baidu.com/f?"
    key = parse.urlencode({"kw": kw})
    url += str(key)
    try:
        tieba_spider(url, beginPage, endPage)
    except error.ContentTooShortError:
        lg.error('downloaded size does not match content-length')
    except error.HTTPError:
        lg.error('occurs HTTP error')
    except error.URLError:
        lg.error('sub-type of OSError')
