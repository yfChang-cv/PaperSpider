from urllib import request
import requests
import time, re, csv
from lxml import etree
from tqdm import tqdm
# from fake_useragent import UserAgent

# 使用http代理
proxies = {
    'https': 'https://127.0.0.1:7890',
    'http': 'http://127.0.0.1:7890'
}

def set_req_proxies(url):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'
        }
        opener = request.build_opener(request.ProxyHandler(proxies))
        request.install_opener(opener)

        req = request.Request(url=url, headers=headers)
        res = request.urlopen(req, timeout=100000)
        # print(res.read().decode())
        # res = requests.get(url=url, headers=headers)
        return res
    except:
        print('重试3此后，仍无法链接。')
        return None
def set_req_old(url):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'
        }

        req = request.Request(url=url, headers=headers)
        res = request.urlopen(req, timeout=100000)
        return res
    except:
        print('重试3此后，仍无法链接。')
        return None


def get_num(s, cont) -> int:
    try:
        return int(re.findall(r'{}'.format(s), cont)[0])
    except:
        return 0


def strprocess(s: str):
    s = s.replace('/n', '')
    s = s.strip()
    return s


def get_data(idx, url):
    res = set_req_old(url=url)
    if res is None:
        return None
    # print(res)

    paper_page = res.read().decode()

    paper_e = etree.HTML(paper_page)

    try:
        papertitle = paper_e.xpath('//div[@id="papertitle"]/text()')[0]
        papertitle = strprocess(papertitle)
    except:
        papertitle = ' '
    try:
        abstract = paper_e.xpath('//div[@id="abstract"]/text()')[0]
        abstract = strprocess(abstract)
    except:
        abstract = ' '

    try:
        authors = paper_e.xpath('//div[@id="authors"]//i/text()')[0]
        authors = strprocess(authors)
        authors = authors.replace(',', '.')
    except:
        authors = ' '

    try:
        pdf_url = paper_e.xpath('//dd//a[text()="pdf"]/@href')[0]
        pdf_url = head + pdf_url
    except:
        pdf_url = ' '

    try:
        arxiv_url = paper_e.xpath('//dd//a[text()="arXiv"]/@href')[0]
    except:
        arxiv_url = ' '

    con = [str(idx), papertitle, authors, abstract, pdf_url, arxiv_url, url]

    try:
        if idx == 0:
            with open(filename, 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(con)
        else:
            with open(filename, 'a', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(con)

    except:
        with open('spider_paper_error.txt', 'a', encoding='utf-8') as f:
            f.write(f'++++++++{idx}--{papertitle}存储错误++++++++\n')

    time.sleep(0.01)


def get_page_con(url):
    res = set_req_old(url=url)
    # print(res)
    base_html = res.read().decode()
    # base_html = res.text
    base_e = etree.HTML(base_html)

    href = base_e.xpath("//dt[@class='ptitle']//@href")
    # pub_time = base_e.xpath("//span[@class='ml']/text()")
    i = 0
    spider_bar = tqdm(href, total=len(href), ncols=100)
    for con_url in spider_bar:
        get_data(i, head + con_url)
        if i % 100 == 0:
            print(f'==爬完{i} {con_url}的数据==')
        i += 1


if __name__ == '__main__':
    head = 'https://openaccess.thecvf.com'
    url = "https://openaccess.thecvf.com/CVPR2022?day=all"
    filename = 'cvpr2022.csv'
    # get_data(10, 'https://openaccess.thecvf.com/content/CVPR2023/html
    # /Ci_GFPose_Learning_3D_Human_Pose_Prior_With_Gradient_Fields_CVPR_2023_paper.html')

    print('开始爬取')
    get_page_con(url=url)
    print('爬取结束')
