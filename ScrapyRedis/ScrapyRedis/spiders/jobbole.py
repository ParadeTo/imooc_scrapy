# -*- coding: utf-8 -*-
from urllib import parse

from scrapy import Request
from scrapy_redis.spiders import RedisSpider


class MySpider(RedisSpider):
    name = 'jobbole'
    allowed_domains = ["blog.jobbole.com", "www.jobbole.com"]
    start_urls = ['http://blog.jobbole.com/all-posts']
    redis_key = 'jobbole:start_urls'

    def parse(self, response):
        """
        1. 列表页所有文章url解析并进行具体字段的解析
        2. 获取下一页的url并交给scrapy进行下载，下载完成后交给parse函数
        """

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
        pass