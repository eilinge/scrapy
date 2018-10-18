# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
from Images.settings import USER_AGENT
import json
import pdb

class ImagesSpider(scrapy.Spider):
    BASE_URL = 'http://image.so.com/zj?ch=beauty&sn=%s&listtype=new&temp=1'
    start_index = 0

    MAX_DOWNLOAD_NUM = 100

    name = 'images'

    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        'Content-Length': '11',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Host': 'image.so.com',
        'Origin': 'http://image.so.com',
        'Referer': 'http://image.so.com/zj?ch=beauty&sn=%s&listtype=new&temp=1',
        'User-Agent': USER_AGENT,
        'X-Requested-With': 'XMLHttpRequest',

    }
    #start_url = BASE_URL
    start_urls = [BASE_URL % 0]
    #allowed_domains = ['image.so.com']
    #start_urls = ['http://image.so.com/']

    #pdb.set_trace()

    def parse(self, response):
        #pass
        #pdb.set_trace()
        infos = json.loads(response.body.decode('utf8'))

        yield {'image_urls':[info['qhimg_url'] for info in infos['list']]}

        self.start_index += infos['count']

        if infos['count'] > 0 and self.start_index < self.MAX_DOWNLOAD_NUM:
            yield Request(self.BASE_URL % self.start_index)
            #yield Request(self.BASE_URL)
