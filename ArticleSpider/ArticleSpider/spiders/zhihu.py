# -*- coding: utf-8 -*-
import json
import re
import scrapy
from scrapy.http import Request
from scrapy.loader import ItemLoader
from items import ZhihuQuestionItem, ZhihuAnswerItem

try:
    import urlparse as parse
except:
    from urllib import parse

class ZhihuSpider(scrapy.Spider):
    name = "zhihu"
    allowed_domains = ["www.zhihu.com"]
    start_urls = ['https://www.zhihu.com/']

    # answer的第一页请求url
    start_answer_url = """https://www.zhihu.com/api/v4/questions/{0}/answers?
    sort_by=default&include=data%5B%2A%5D.is_normal%2Cis_sticky%2Ccollapsed_by%2
    Csuggest_edit%2Ccomment_count%2Ccan_comment%2Ccontent%2Ceditable_content%2
    Cvoteup_count%2Creshipment_settings%2Ccomment_permission%2Cmark_infos%2C
    created_time%2Cupdated_time%2Crelationship.is_authorized%2Cis_author%2Cvoting
    %2Cis_thanked%2Cis_nothelp%2Cupvoted_followees%3Bdata%5B%2A%5D.author.is_blocking%2C
    is_blocked%2Cis_followed%2Cvoteup_count%2Cmessage_thread_token%2Cbadge%5B%3F%28type%3Dbest_answerer%29%5D.topics&limit={1}&offset={2}"""

    headers = {
        "Accept": "*/*",
        "Accept-Encoding": "gzip,deflate",
        "Accept-Language": "en-US,en;q=0.8,zh-TW;q=0.6,zh;q=0.4",
        "Connection": "keep-alive",
        "Content-Type":" application/x-www-form-urlencoded; charset=UTF-8",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.111 Safari/537.36",
        "Referer": "http://www.zhihu.com/",
        "HOST": "www.zhihu.com",
    }

    cookies = {
        'aliyungf_tc': 'AQAAABx1uDOkTQYASMn6OsSlYtv8kybR',
        'q_c1': 'aa5680616f0245e79f492f6ad4688417|1491363434000|1491363434000',
        '_xsrf': 'cf17fae17fa12a3e8adf7e2253411f88',
        'r_cap_id':'"YThjODQxMWMyMjMwNGNjMTk5OWQ1ZjEzNmNjOWJjMzk=|1491375616|7011cd4a39779bf3c0cdf4bb70020fed8f4d2884"',
        'cap_id': '"MGFlZDM2OTY0Y2VkNGZiMjlhN2ViZDg4MzliODBlNTI=|1491375616|c48934d6abc7dff6ace07b3000f9dfa6d2505bfa"',
        'd_c0': '"AFDCeq8fjwuPTlQiq4rK8DapC2xEnelD_gc=|1491363434"',
        '_zap': 'b44ab878-901b-4d52-936e-6b5466cbaf95',
        'l_n_c': '1',
        'z_c0': 'Mi4wQUVDQzNJWFlod3NBVU1KNnJ4LVBDeGNBQUFCaEFsVk5GU01NV1FBSGVhaGNEVm5UZDFKZEJrRThVV2F4OWFNRkJ3|1491375647|b4943a399a0daee0ab0a364542d832db7e50d89f',
        '__utmt': '1',
        '__utma': '51854390.14300998.1491362939.1491362939.1491372580.2',
        '__utmb': '51854390.2.10.1491372580',
        '__utmc': '51854390',
        '__utmz': '51854390.1491372580.2.2.utmcsr=baidu|utmccn=(organic)|utmcmd=organic',
        '__utmv': '51854390.100--|2=registration_date=20170330=1^3=entry_date=20170330=1'
    }

    def parse(self, response):
        """
        提取出页面中的所有url，并跟踪爬取，
        如果url中格式为/question/xxx 就下载之后进入解析函数
        """
        all_urls = response.css("a::attr(href)").extract()
        all_urls = [parse.urljoin(response.url, url) for url in all_urls]
        # 过滤javascript:;
        all_urls = filter(lambda x: True if x.startswith("https") else False, all_urls)

        # 深度优先
        for url in all_urls:
            match_obj = re.match("(.*zhihu.com/question/(\d+))(/|$).*", url)
            if match_obj:
                # 如果提取到question相关的页面，则下载后交由提取函数处理
                request_url = match_obj.group(1)
                question_id = match_obj.group(2)

                # 提交给下载器
                yield scrapy.Request(request_url, headers=self.headers, callback=self.parse_question)

            else:
                # 如果不是，则直接进一步跟踪
                yield scrapy.Request(url, cookies=self.cookies, headers=self.headers)

    def parse_question(self, response):
        """处理question页面，从页面中提取出具体的question item"""

        match_obj = re.match("(.*zhihu.com/question/(\d+))(/|$).*", response.url)
        if match_obj:
            question_id = int(match_obj.group(2))

        if "QuestionHeader-title" in response.text:
            # 处理新版本
            item_loader = ItemLoader(item=ZhihuQuestionItem(), response=response)
            item_loader.add_css("title", "h1.QuestionHeader-title::text")
            item_loader.add_css("content", ".QuestionHeader-detail")
            item_loader.add_value("url", response.url)
            item_loader.add_value("zhihu_id", question_id)
            item_loader.add_css("answer_num", ".List-headerText span::text")
            item_loader.add_css("comments_num", ".QuestionHeader-actions button::text")
            item_loader.add_css("watch_user_num", ".NumberBoard-value::text")
            item_loader.add_css("topics", ".QuestionHeader-topics .Popover div::text")

            question_item = item_loader.load_item()
        else:
            # 旧版本
            item_loader = ItemLoader(item=ZhihuQuestionItem(), response=response)
            # item_loader.add_css("title", ".zh-question-title h2 a::text")
            item_loader.add_xpath("title", "//*[@class='zh-question-title']/h2/a/text()|//*[@class='zh-question-title']/h2/span/text()")
            item_loader.add_css("content", "#zh-question-detail")
            item_loader.add_value("url", response.url)
            item_loader.add_value("zhihu_id", question_id)
            item_loader.add_css("answer_num", "#zh-question-answer-num::text")
            item_loader.add_css("comments_num", "#zh-question-meta-wrap a[name='addcomment']::text")
            # item_loader.add_css("watch_user_num", "#zh-question-side-header-wrap::text")
            item_loader.add_xpath("watch_user_num", "//*[@id='zh-question-side-header-wrap']/text()|//*[@class='zh-question-followers-sidebar']/div/a/strong/text()")
            item_loader.add_css("topics", ".zm-tag-editor-labels a::text")

            question_item = item_loader.load_item()

        yield scrapy.Request(self.start_answer_url.format(question_id))

        # 提交给pipeline
        yield question_item

    def start_requests(self):
        # 重写
        # 方法一，加入cookie
       yield scrapy.Request('https://www.zhihu.com/', cookies=self.cookies, headers=self.headers)
        # 方法二，登录
        # return [scrapy.Request('https://www.zhihu.com/#signin', headers=self.headers, callback=self.login)] # callback默认为parse

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
        text_json = json.loads(response.text)
        if "msg" in text_json and text_json["msg"] == '登录成功':
            for url in self.start_urls:
                yield self.make_requests_from_url(url)