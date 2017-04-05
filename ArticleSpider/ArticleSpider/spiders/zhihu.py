# -*- coding: utf-8 -*-
import re
import scrapy

try:
    import urlparse as parse
except:
    from urllib import parse

class ZhihuSpider(scrapy.Spider):
    name = "zhihu"
    allowed_domains = ["www.zhihu.com"]
    start_urls = ['http://www.zhihu.com/']
    headers = {
        "HOST": "www.zhihu.com",
        "Referer": "www.zhihu.com",
        "User-Agent": 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
    }

    def parse(self, response):
        """
        提取出页面中的所有url，并跟踪爬取，
        如果url中格式为/question/xxx 就下载之后进入解析函数
        """
        all_urls = response.css("a::attr(href)").extract()
        all_urls = [parse.urljoin(response.url, url) for url in all_urls]
        for url in all_urls:
            pass

    def start_requests(self):
        # 重写
        return [scrapy.Request('https://www.zhihu.com/#signin', headers=self.headers, callback=self.login)] # callback默认为parse

    def login(self, response):
        response_text = response.text
        match_obj = re.match('[\s\S]*name="_xsrf" value="(.*?)"', response_text)
        xsrf = ''
        if match_obj:
            xsrf = match_obj.group(1)

        if xsrf:
            post_url = "https://www.zhihu.com/login/phone_num"
            post_data = {
                "_xsrf": xsrf,
                "phone_num": "18611112949",
                "password": "81051766"
            }

            return [scrapy.FormRequest(
                url=post_url,
                formdata=post_data,
                headers=self.headers,
                callback=self.check_login
            )]

    def check_login(self, response):
        # 验证服务器的返回数据判断是否成功
        pass