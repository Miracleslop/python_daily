from urllib import request
from urllib import parse
from urllib import error
from commun.logger import clog

lg = clog.Logger("web_spider")


@clog.log('downloading...', lg)
def load_page(url):
    head = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/64.0.3282.140 Safari/537.36 Edge/17.17134 "
    }
    rqs = request.Request(url, headers=head)
    rqs.add_header("Connection", "keep-alive")
    rps = request.urlopen(rqs)
    html = rps.read()
    return html


@clog.log('writing...', lg)
def write_file(content, path):
    str_content = str(content)
    with open(path, 'w') as f:
        f.write(str_content)


@clog.log('spidering...', lg)
def tieba_spider(url, begin_page, end_page):
    """
        作用：负责处理url，分配每个url去发送请求
        url：需要处理的第一个url
        beginPage: 爬虫执行的起始页面
        endPage: 爬虫执行的截止页面
    """

    for page in range(begin_page, end_page + 1):
        pn = (page - 1) * 50

        filename = "page " + str(page) + ".html"
        full_url = '%s&pn=%d' % (url, pn)

        html = load_page(full_url)
        write_file(html, filename)


if __name__ == "__main__":
    kw = "lol"
    beginPage = 0
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