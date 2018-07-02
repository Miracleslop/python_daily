from urllib.request import *
from commun.logger import Logger
lg = Logger.Logger("web_crawler")


def load_page(url):
    print('is downloading...')
    head = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/64.0.3282.140 Safari/537.36 Edge/17.17134 "
    }
    request = Request(url, headers=head)
    request.add_header("Connection", "keep-alive")
    response = urlopen(request)
    html = response.read()
    return html


def write_file(content, path):
    print('is writing...')
    with open(path, 'w') as f:
        f.write(content)



def tieba_spider(url, beginPage, endPage):
    """
        作用：负责处理url，分配每个url去发送请求
        url：需要处理的第一个url
        beginPage: 爬虫执行的起始页面
        endPage: 爬虫执行的截止页面
    """

    for page in range(beginPage, endPage + 1):
        pn = (page - 1) * 50

        filename = "page " + page + ".html"
        fullurl = url + "&pn=" + pn

        html = load_page(fullurl)
        write_file(html, filename)


if __name__ == "__main__":
    kw = "lol"
    beginPage = 0
    endPage = 5
    url = "http://tieba.baidu.com/f?"
    key = {"kw": kw}
    url += key
