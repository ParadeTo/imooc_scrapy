# -*- coding: utf-8 -*-
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from scrapy_redis.spiders import RedisCrawlSpider


class LagouSpider(RedisCrawlSpider):
    """
    不能重载parse函数
    """
    name = 'jobbole_crawl'
    # allowed_domains = ['blog.jobbole.com']
    # start_urls = ['http://blog.jobbole.com/all-posts']
    redis_key = 'jobbole_crawl:start_urls'

    rules = (
        # 抽取link的规则 process_links 对link 的预处理
        Rule(LinkExtractor(allow=r'blog.jobbole.com/\d+'), callback='parse_detail', follow=True),
    )

    def parse_detail(self, response):
        """
              提取文章的具体字段
              """
        pass