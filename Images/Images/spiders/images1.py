# -*- coding: utf-8 -*-
import scrapy
from scrapy.pipelines.images import ImagesPipeline
from Images.settings import USER_AGENT
from Images.items import ImagesItem
import json
import pdb

class ImagesSpider(scrapy.Spider):
    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'Connection': 'keep-alive',
        'Content-Length': '11',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Host': 'image.so.com',
        'Origin': 'http://image.so.com',
        'Referer': 'http://image.so.com/zj?ch=beauty&sn=%s&listtype=new&temp=l',
        # 'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5',
        'User-Agent': USER_AGENT,
        'X-Requested-With': 'XMLHttpRequest',

    }

    base_url = 'http://image.so.com/zj?ch=beauty&sn=%s&listtype=new&temp=1'
    name = 'images'

    start_index = 0
    #allowed_domains = ['image.so.com']
    start_urls = [ base_url % 0 ]

    MAX_LOADER_NUM = 100

    def parse(self, response):
        #pass
        images = ImagesItem()
        #pdb.set_trace()
        res = json.loads(response.body.decode('utf8'))
        #for sel in res['list']:
            #print sel
            #images['images_url'] = sel['qhimg_url']
            #yield images
            #yield scrapy.Request(images['images_url'].decode('utf8'))
        yield {'images_url':[sel['qhimg_url'] for sel in res['list']]}

        #pdb.set_trace()
        self.start_index += res['count']
        if res['count'] >0 and self.start_index < self.MAX_LOADER_NUM:
            yield scrapy.Request(self.base_url % self.start_index)
