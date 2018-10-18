# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import scrapy
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exceptions import DropItem
from dbmeinv.items import DbmeinvItem
import pdb

class DbmeinvPipeline(ImagesPipeline):
    #def process_item(self, item, spider):
        #return item

    def get_media_requests(self,item,info):
        #pdb.set_trace()
        yield scrapy.Request(item['images_url'])

    def item_completed(self,results,item,info):
        images_paths = [x['path'] for ok,x in results if ok]

        if not images_paths:
            raise DropItem("Item contains no images")

        return item


class DuplicatesPipeline(object):
    def __init__(self):
        self.ids_seen = set()

    def process_item(self, item, spider):
        if item['images'] in self.ids_seen:
            raise DropItem("Duplicate item found: %s" % item)
        else:
            self.ids_seen.add(item['images'])
            return item
