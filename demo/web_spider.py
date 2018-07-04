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

    def __skip_script(self, i):
        """
        从下标i开始匹配<script>...</script>，并过滤
        :param i:开始匹配的text下标 
        :return:返回-1表示匹配失败，否则返回</script>后面第一个字符的下标
        """
        self.__end_sign = ['</script>', '<html>', '</html>', '<head>', '</head>']
        scr_str = '<script>'
        scr_len = len(scr_str)
        if self.__text[i:i + scr_len] != scr_str:
            return -1

        # i调转到<script>后面第一个字符的下标
        i += scr_len

        # 搜寻</script>
        while i < self.__len:
            if self.__text[i] == '<' and self.__text[i + 1] != '!':
                try:
                    tag_end_in = self.__text.index('>', i)
                    tag_str = self.__text[i:tag_end_in + 1]
                    self.__end_sign.index(tag_str)
                    i = tag_end_in + 1
                    break
                except ValueError:
                    pass
            i += 1
        return i

    def __skip_annotation(self, i):
        end_sign = "-->"
        ann_str = "<!--"
        ann_len = len(ann_str)
        if self.__text[i:i + ann_len] != ann_str:
            return -1
        i += ann_len
        while i < self.__len:
            if self.__text[i] == '>':
                if self.__text[i - 2:i + 1] == end_sign:
                    i += 1
                    break
            i += 1
        return i

    @clog.log('filter script content ! ', lg)
    def filter(self):

        io_text = io.StringIO()
        old_i = 0
        i = 0
        while i < self.__len:
            if self.__text[i] == '<':

                # 判断<script>...</script>，并过滤
                scp_sign = self.__skip_script(i)
                if scp_sign != -1:
                    io_text.write(self.__text[old_i:i])
                    i = scp_sign
                    old_i = scp_sign
                    continue

                # 判断<!-- ...  --> ，并过滤
                ann_sign = self.__skip_annotation(i)
                if ann_sign != -1:
                    io_text.write(self.__text[old_i:i])
                    i = ann_sign
                    old_i = ann_sign
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
