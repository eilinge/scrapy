# -*- coding: utf-8 -*-
import scrapy
import pdb
import json
from Jike.settings import USER_AGENT
import re
import urllib
from Jike.items import JikeItem

class JikeSpider(scrapy.Spider):
    name = 'jike'
    allowed_domains = ['api.geetest.com']
    start_urls = ['https://api.geetest.com/refresh.php?gt=b6e21f90a91a3c2d4a31fe84e10d0442&challenge=93d8c247b5b4701a85970d6593aeb3e5ie&lang=zh-cn&type=multilink&callback=geetest_1538117289792']

    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        'Content-Length': '11',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Host': 'api.geetest.com',
        #'Origin': 'api.geetest.com',
        #'Referer': 'https://api.geetest.com/refresh.php?gt=b6e21f90a91a3c2d4a31fe84e10d0442&challenge=93d8c247b5b4701a85970d6593aeb3e5ie&lang=zh-cn&type=multilink&callback=geetest_1538117289792',
        'User-Agent': USER_AGENT,
        'X-Requested-With': 'XMLHttpRequest',

    }

    def parse(self, response):
        #pdb.set_trace()
        a = response.body
        url_list = []
        jike = JikeItem()
        #jsonload = json.loads(response.body.decode('utf8'))#.encode('utf8')
        jike['name'] = 'https://static.geetest.com/' + re.findall(r'"bg": "(.*?\.jpg)',a)[0]
        jike['name'] = 'https://static.geetest.com/' + re.findall(r'"fullbg": "(.*?\.jpg)',a)[0]
        #rllib.urlretrieve(bg_url,'./bg.jpg')
        #print jsonload
        #pass
        return jike
