# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pdb
import scrapy
from scrapy.pipelines.images import ImagesPipeline

class DoutuPipeline(ImagesPipeline):
    #def process_item(self, item, spider):
        #return item

    def get_media_requests(self, item, info):

        #for image_url in item['image_urls']:
            #pdb.set_trace()
            #yield scrapy.Request(image_url)
        yield scrapy.Request(item['image_urls'])

    def item_completed(self, results, item, info):

        image_paths = [x['path'] for ok, x in results if ok]  # ok判断是否下载成功

        if not image_paths:
            raise DropItem("Item contains no images")
        # item['image_paths'] = image_paths
        return item

