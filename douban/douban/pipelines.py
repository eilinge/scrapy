# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import scrapy
from scrapy.pipelines.images import ImagesPipeline
import pdb

class DoubanPipeline(ImagesPipeline):
    #def process_item(self, item, spider):
        #return item

    def get_media_requests(self,item,info):
        pdb.set_trace()
        yield scrapy.Request(item['image_urls'])
