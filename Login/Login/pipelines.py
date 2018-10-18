# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pdb
import scrapy
from scrapy.pipelines.files import FilesPipeline
from scrapy.pipelines.images import ImagePipeline

class LoginPipeline(object):
    def process_item(self, item, spider):
        return item
