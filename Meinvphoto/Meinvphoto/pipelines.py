# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import scrapy
from scrapy.pipelines.images import ImagesPipeline
import urlparse
from os.path import basename,dirname,join
import pdb

'''
class MeinvphotoPipeline(object):
    def process_item(self, item, spider):
        return item
'''

class MeinvphotoPipeline(ImagesPipeline):
    def file_path(self,request,response=None,info=None):
        path = urlparse.urlparse(request.url).path
        #pdb.set_trace()
        return join(basename(dirname(path)),basename(path))

    def get_media_requests(self,item,info):
        yield scrapy.Request(item['images_url'])
