# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import scrapy
import pdb
from scrapy.item import Item
from scrapy.exceptions import DropItem
import pymongo
import pdb


class BooksPipeline(object):
    def process_item(self, item, spider):
        return item

class Price_convertPipeline(object):
    price_rate = 8.04
    def process_item(self,item,spider):
        #price_old = item['price']
        #pdb.set_trace()
        price_new = self.price_rate * float(item['price'][1:])
        item['price'] = '$%.2f'%price_new
        return item

class DuplicatePipeline(object):
    def __init__(self):
        self.set = set()

    def process_item(self,item,spider):
        name = item['name']
        if name in self.set:
            raise DropItem('Duplicate book found:%s'%item)

        self.set.add(name)
        return item

class MongoDBPipeline(object):
    @classmethod
    def from_crawler(cls,crawler):
        cls.DB_URL = crawler.settings.get('MONGO_DB_URL','mongodb://localhost:27017/')
        cls.DB_NAME = crawler.settings.get('MONGO_DB_NAME','scrapy_data')
        return cls()
    def open_spider(self,spider):
        self.client = pymongo.MongoClient(self.DB_URL)
        self.db     = self.client[self.DB_NAME]
    def close_spider(self,spider):
        self.client.close()
    def process_item(self,item,spider):
        #pdb.set_trace()
        collections = self.db[spider.name]
        post = dict(item) if isinstance(item,Item) else item
        collections.insert_one(post)
        return item

class RedisPipeline(object):
    def open_spider(self,spider):
        db_host = spider.settings.get('REDIS_HOST','localhost')
        db_port = spider.settings.get('REDIS_PORT',6379)
        db_index = spider.settings.get('REDIS_DB_INDEX',0)
        self.item_i = 0
        self.db_conn = redis.StrictRedis(host=db_host,port=db_port,index=db_index)

    def close_spider(self,spider):
        self.db_conn.connection_pool.disconnect()

    def process_item(self,item,spider):
        post = dict(item) if isintance(item,Item) else item
        self.item_i += 1
        self.db_conn.hmset('book:%s'%self.item_i,post)

        return item