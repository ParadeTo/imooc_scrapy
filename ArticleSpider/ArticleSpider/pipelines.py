# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.pipelines.images import ImagesPipeline
from scrapy.exporters import JsonItemExporter
from twisted.enterprise import adbapi

import codecs
import json
import MySQLdb
import MySQLdb.cursors


class ArticlespiderPipeline(object):
    def process_item(self, item, spider):
        return item

class JsonWithEncodingPipeline(object):
    # 自定义json文件的导出
    def __init__(self):
        self.file = codecs.open('article.json', 'w', encoding="utf-8")

    def process_item(self, item, spider):
        lines = json.dumps(dict(item), ensure_ascii=False) + '\n'
        self.file.write(lines)
        return item

    def spider_closed(self, spider):
        self.file.close()

class JsonExporterPipeline(object):
    # 调用scrapy提供的json exporter 导出json文件
    def __init__(self):
        self.file = open('articleexport.json', 'wb')
        self.exporter = JsonItemExporter(self.file, encoding="utf-8", ensure_ascii=False)
        self.exporter.start_exporting()

    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.file.close()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item

class MysqlPipeline(object):
    # 这里是同步的操作，有可能后期插入速度跟不上爬取速度
    def __init__(self):
        self.conn = MySQLdb.connect('127.0.0.1', 'root', '123456', 'scrapy', charset="utf8", use_unicode=True)
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        insert_sql = """
            insert into jobbole (title, url, url_object_id, create_date, fav_nums)
            VALUES (%s, %s, %s, %s, %s)
        """
        self.cursor.execute(insert_sql, (item['title'], item['url'], item['url_object_id'], item['create_date'], item['fav_nums']))
        self.conn.commit()

class MysqlTwistedPipeline(object):
    def __init__(self, dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls, settings):
        """
        关于staticmethod和classmethod的区别
        http://stackoverflow.com/questions/12179271/meaning-of-classmethod-and-staticmethod-for-beginner
        """
        dbparams = dict(
            host = settings['MYSQL_HOST'],
            db = settings['MYSQL_DBNAME'],
            user = settings['MYSQL_USER'],
            passwd = settings['MYSQL_PASSWORD'],
            charset = "utf8",
            cursorclass = MySQLdb.cursors.DictCursor,
            use_unicode = True
        )

        dbpool = adbapi.ConnectionPool("MySQLdb", **dbparams)

        return cls(dbpool)

    def process_item(self, item, spider):
        """
        使用twisted将mysql插入变成异步执行
        """
        query = self.dbpool.runInteraction(self.do_insert, item)
        query.addErrback(self.handle_error, item, spider)

    def handle_error(self, failure):
        """
        处理异步插入的异常
        """
        print (failure)

    def do_insert(self, cursor, item):
        insert_sql = """
            INSERT INTO jobbole (title, url, url_object_id, create_date, fav_nums)
            VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(insert_sql, (item['title'], item['url'], item['url_object_id'], item['create_date'], item['fav_nums']))


class ArticleImagePipeline(ImagesPipeline):
    def item_completed(self, results, item, info):
        # 有这个字段才处理
        if "front_image_url" in item:
            for ok, value in results: # 其实只有一个
                image_file_path = value["path"]
            item['front_image_path'] = image_file_path
            return item