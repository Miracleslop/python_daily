from urllib import request
from urllib import parse
from urllib import error
from commun.logger import clog
from demo.webSpider.htmlity import HtmlTagStart
from demo.webSpider.htmlity import HtmlTagEnd
import io

lg = clog.Logger("web_spider")


class FilterStrategy(object):

    def __init__(self, text: str):
        """
        :param text:  待过滤的文本
        """
        self.__text = text
        self.__len = len(text)

        # 过滤选项，key统一为前4个字符，value为HtmlTag的子类对象
        self.__switch = {
            '<scr': HtmlTagStart('<script', '</script>'),
            '<!--': HtmlTagEnd('<!--', '-->'),
            '<lin': HtmlTagEnd('<link', '/>'),
            '<cod': HtmlTagStart('<code', '</code>')
        }

    @clog.log('filter script content ! ', lg)
    def filter(self):
        """
        过滤主体
        :return: 返回过滤后的文本:str
        """
        # 存储过滤后的文本
        io_text = io.StringIO()

        # 记录需要跳过部分的起始id
        old_i = 0

        # 遍历文本的下标
        i = 0
        while i < self.__len:
            # 判断是否是过滤文本的开头
            if self.__text[i] == '<':

                # 取出长度为4的字符串判断是否存在于过滤选项中
                sel = self.__switch.get(self.__text[i:i + 4])
                if sel is not None:
                    sel_len = sel.start_len
                    if self.__text[i:i + sel_len] == sel.start_sign:
                        # 存在过滤选项中，开始过滤

                        # 存储过滤文本之前的字符串内容到内存中
                        io_text.write(self.__text[old_i:i])

                        # i调转到<script后面第一个字符的下标
                        i += sel_len

                        # 开始遍历直到结束标记为止
                        i = sel.skip_content(i, self.__text)

                        # 此时i已经跳到结束标记的后一个字符，并将此处记为old_i
                        old_i = i

                        # 此时i已经在新的字符上，所以直接continue
                        continue
            i += 1

        res_text = io_text.getvalue()
        io_text.close()
        return res_text


class Demo(object):
    @clog.log('downloading...', lg)
    def _load_page(self, req_url: str):
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
        # 解析读取后的字节文件为字符串
        html_str = html_byte.decode('utf-8')
        return html_str

    @clog.log('writing...', lg)
    def _write_file(self, content: str, path):
        """
        作用：把str写入相应路径的文件
        :param content:需要写入的str
        :param path: 写入文件的路径
        :return:写入结束不返回值
        """
        with open(path, 'w') as f:
            f.write(content)

    @clog.log('spidering...', lg)
    def tieba_spider(self, req_url, begin_page, end_page):
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

            # 爬去指定url的页面，并返回未解析的html信息
            html_str = self._load_page(full_url)
            # 创建过滤对象
            fs = FilterStrategy(html_str)
            # 过滤并将返回值转成字符串
            html_fil = str(fs.filter())
            # 将过滤后的内容写入文本文件
            self._write_file(html_fil, filename)


if __name__ == "__main__":
    kw = "lol"
    beginPage = 1
    endPage = 1
    url = "http://tieba.baidu.com/f?"
    key = parse.urlencode({"kw": kw})
    url += str(key)
    try:
        demo = Demo()
        demo.tieba_spider(url, beginPage, endPage)
    except error.ContentTooShortError:
        lg.error('downloaded size does not match content-length')
    except error.HTTPError:
        lg.error('occurs HTTP error')
    except error.URLError:
        lg.error('sub-type of OSError')


