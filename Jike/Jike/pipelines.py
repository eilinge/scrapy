# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import scrapy
from scrapy.pipelines.images import ImagesPipeline
import pdb

class JikePipeline(object):
    def process_item(self, item, spider):
        return item

class JikeImagePipeline(ImagesPipeline):

    def get_media_requests(self,item,spider):
        #pdb.set_trace()
        yield scrapy.Request(item['name'])