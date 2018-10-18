# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import scrapy
import pdb
from scrapy.pipelines.files import FilesPipeline
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exceptions import DropItem
from scrapy.items import Item
import pymongo

class Price_convertPipeline(object):
    pirce_rate = 0.784
    def process_item(self,item,spider):
        price_old = item['price']
        new_price = float(price_old[1:]) * self.price_rate
        item['price'] = '$%s.2f'%new_price
        return item

class DuplicatePipeline(object):
    def __init__(self):
        self.set = set()
    def process_item(self,item,spider):
        name = item['name']
        if name in self.set():
            raise DropItem('Dupelicate the items is%s'%item)

        self.set.add(name)
        return item

class MongoDBPipeline(object):
    @classmethod
    def from_crawler(cls,crawler):
        cls.DB_URL = crawler.settings.get('MONGO_DB_URL','mongodb://localhost:27017')
        cls.DB     = crawler.settings.get('MONGO_DB_name','scrapy_data')

        return cls()
    def open_spider(self,spider):
        self.db_client = pymongo.MongoDBCilent(self.DB_URL)
        self.db        = self.db_client[self.DB]

    def close_spider(self,spider):
        self.db_client.close()

    def process_item(self,item,spider):
        collections = self.db[spider.name]
        post = dict(item) if isintance(item,Item) else item
        collections.insert_one(post)

        return item