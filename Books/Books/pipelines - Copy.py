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
        cls.db_url  = crawler.settings.get('MONGO_DB_URL','mongodb:http//localhsot:67017')
        cls.db_name = crawler.settings.get('MONGO_DB_NAME','scrapy_data')
        return cls()
    def from_spider(self,spider):
        self.conn_db = pymongo.MongoClinet(self.db_url)
        self.db      = self.conn_db[self.db_name]

    def close_spider(self,spider):
        self.conn_db.close()
    def process_item(self,item,spider):
        collection = self.conn_db[spider['name']]
        post = dict(item) if isintance(item,Item) else item
        collection.insert_one(post)
        return item

class RedisPipeline(object):
    def open_spider(self,spider):
        db_host = spider.settings.get('REDIS_HOST','localhost')
        db_port = spider.settings.get('REDIS_PORT',6379)
        db_index= spider.settings.get('REDIS_INDEX',0)
        db_passwd=spider.settings.get('REDIS_PASSWD','redis')
        self.item_i = 0
        self.db_conn = redis.StrictRedis(host=db_host,port=db_port,index=db_index,passwd=db_passwd)
    def close_spider(self,spider):
        self.db_conn.connection_pool.disconnect()
    def process_item(self,item,spider):
        post = dict(item) if isintance(item,Item) else item
        self.item_i += 1
        db_conn.hmset('book:%s'%self.item_i,post)
        return item