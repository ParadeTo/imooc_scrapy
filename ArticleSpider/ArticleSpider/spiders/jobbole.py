# -*- coding: utf-8 -*-
import scrapy
import re
import datetime

from scrapy.http import Request
from scrapy.loader import ItemLoader
from scrapy.xlib.pydispatch import dispatcher
from scrapy import signals

from ArticleSpider.items import JobBoleArticleItem
from ArticleSpider.utils.common import get_md5
from ArticleSpider.items import ArticleItemLoader

from selenium import webdriver
from urllib import parse

class JobboleSpider(scrapy.Spider):
    name = "jobbole"
    allowed_domains = ["blog.jobbole.com"]
    start_urls = ['http://blog.jobbole.com/all-posts/']
    # start_urls = ['http://xazkkj.eicp.net/']

    # 信号处理
    # def __init__(self):
    #     self.browser = webdriver.Chrome(executable_path="e:/soft/selenium/chromedriver.exe")
    #     super(JobboleSpider, self).__init__()
    #     dispatcher.connect(self.spider_closed, signals.spider_closed) # 类似于js的事件，当spider关闭时执行    #self.spider_closed
    #
    # def spider_closed(self, spider):
    #     # 爬虫退出时关闭chrome
    #     self.browser.quit()

    # 收集404的url和404页面数，没有下面这个直接不会处理404的页面
    handle_httpstatus_list = [404]

    def __init__(self):
        self.fail_urls = []
        dispatcher.connect(self.handle_spider_closed, signals.spider_closed)

    # 爬虫结束时调用这个方法
    def handle_spider_closed(self, spider, reason):
        self.crawler.stats.set_value('failed_urls', ','.join(self.fail_urls))

    def parse(self, response):
        """
        1. 列表页所有文章url解析并进行具体字段的解析
        2. 获取下一页的url并交给scrapy进行下载，下载完成后交给parse函数
        """
        if response.status == 404:
            self.fail_urls.append(response.url)
            self.crawler.stats.inc_value('failed_url')

        # 解析列表页中的所有url
        post_nodes = response.css("#archive .floated-thumb .post-thumb a")
        for post_node in post_nodes:
            image_url = post_node.css("img::attr(src)").extract_first("")
            post_url = post_node.css("::attr(href)").extract_first("")
            yield Request(url=parse.urljoin(response.url, post_url), callback=self.parse_detail, meta={'front_image_url': image_url})

        # 提取下一页并交给scrapy进行下载
        next_url = response.css(".next.page-numbers::attr(href)").extract_first()
        if next_url:
            yield Request(url=parse.urljoin(response.url, post_url), callback=self.parse)


    def parse_detail(self, response):
        """
        提取文章的具体字段
        """
        # article_item = JobBoleArticleItem()
        #
        #
        # title = response.css('.entry-header h1::text').extract_first()
        #
        # create_date = response.xpath('//p[@class="entry-meta-hide-on-mobile"]/text()').extract_first().strip().replace('·','').strip()
        #
        # tag_list = response.xpath('//p[@class="entry-meta-hide-on-mobile"]/a/text()').extract()
        # tag_list = [element for element in tag_list if not element.strip().endswith('评论')]
        # tags = ",".join(tag_list)
        #
        # praise_nums = int(response.xpath("//span[contains(@class, 'vote-post-up')]/h10/text()").extract_first() or 0)
        #
        # fav_nums = response.xpath("//span[contains(@class, 'bookmark-btn')]/text()").extract_first()
        # match_re = re.match(".*?(\d+).*", fav_nums)
        # if match_re:
        #     fav_nums = int(match_re.group(1))
        # else:
        #     fav_nums = 0
        #
        # comment_nums = response.xpath("//a[@href='#article-comment']/span/text()").extract_first()
        # match_re = re.match(".*?(\d+).*", comment_nums)
        # if match_re:
        #     comment_nums = int(match_re.group(1))
        # else:
        #     comment_nums = 0
        #
        # content = response.xpath("//div[@class='entry']").extract_first()
        #
        # article_item['url_object_id'] = get_md5(response.url)
        # article_item['title'] = title
        # article_item['url'] = response.url
        # try:
        #     create_date = datetime.datetime.strptime(create_date, "%Y/%m/%d").date()
        # except Exception as e:
        #     create_date = datetime.datetime.now().date()
        # article_item['create_date'] = create_date
        # article_item['front_image_url'] = [front_image_url]
        # article_item['praise_nums'] = praise_nums
        # article_item['comment_nums'] = comment_nums
        # article_item['fav_nums'] = fav_nums
        # article_item['tags'] = tags
        # article_item['content'] = content

        # 通过itemloader加载item
        front_image_url = response.meta.get("front_image_url", "") # 封面图
        item_loader = ArticleItemLoader(item=JobBoleArticleItem(), response=response)
        item_loader.add_css("title", ".entry-header h1::text")
        item_loader.add_css("create_date", "p.entry-meta-hide-on-mobile::text")
        item_loader.add_css("praise_nums", ".vote-post-up h10::text")
        item_loader.add_css("comment_nums", "a[href='#article-comment'] span::text")
        item_loader.add_css("fav_nums", ".bookmark-btn::text")
        item_loader.add_css("tags", "p.entry-meta-hide-on-mobile a::text")
        item_loader.add_css("content", "div.entry")
        item_loader.add_value("front_image_url",  [front_image_url])
        item_loader.add_value("url", response.url)
        item_loader.add_value("url_object_id", get_md5(response.url))

        article_item = item_loader.load_item()

        yield article_item
