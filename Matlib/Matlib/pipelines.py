# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import scrapy
from scrapy.pipelines.files import FilesPipeline
import urlparse
from os.path import basename,dirname,join
import pdb

'''
class MatlibPipeline(object):

    def process_item(self, item, spider):
        return item

'''
class MyFilePipeline(FilesPipeline):

    def get_media_requests(self,item,info):
        #for file in item['files_url']:
            #yield scrapy.Request(file.encode('utf-8'))
        yield scrapy.Request(item['files_url'])

    def file_path(self, request, response=None, info=None):
        split_url = str(request.url).split('/')
        kind_name = split_url[-2]
        file_name = split_url[-1]
        return '%s/%s' % (kind_name, file_name)


