# -*- coding: utf-8 -*-
import requests
from scrapy.selector import Selector

def crawl_ips():
    # 爬取西刺的免费ip代理
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.111 Safari/537.36"
    }
    re = requests.get("http://www.xicidaili.com/nn/", headers=headers)

    selector = Selector(text=re.text)
    all_trs = selector.css("#ip_list tr")
    print (re.text)

print (crawl_ips())