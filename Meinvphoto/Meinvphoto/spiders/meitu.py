# -*- coding: utf-8 -*-
import scrapy
import pdb
from scrapy.linkextractors import LinkExtractor
from Meinvphoto.items import MeinvphotoItem
from Meinvphoto.settings import USER_AGENT

class MeituSpider(scrapy.Spider):
    name = 'meitu'
    allowed_domains = ['www.27270.com','t2.hddhhn.com']
    start_urls = ['http://www.27270.com/tag/651.html']

    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        'Content-Length': '11',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        #'Host': 'www.27270.com',
        #'Origin': 'www.27270.com',
        'Referer': 'http://www.27270.com/tag/651.html',
        'User-Agent': USER_AGENT,
        'X-Requested-With': 'XMLHttpRequest',

    }

    def parse(self, response):

        le = LinkExtractor(restrict_css='div.w1200.oh')

        for link in le.extract_links(response):
            yield scrapy.Request(link.url,callback=self.parse_photo)

        le1 = LinkExtractor(restrict_css='div.TagPage')
        #pdb.set_trace()
        for link1 in le1.extract_links(response):
            yield scrapy.Request(link1.url,callback=self.parse)

    def parse_photo(self,response):

        photo = MeinvphotoItem()
        if response.css('div.articleV4Body img::attr(src)').extract():
            photo['images_url'] = response.css('div.articleV4Body img::attr(src)').extract()[0].encode('utf8')

        #pdb.set_trace()
        #'''
        pattern = r'_\d\.html$'
        le2 = LinkExtractor(allow=pattern)
        for link2 in le2.extract_links(response):
            #pdb.set_trace()
            yield scrapy.Request(link2.url,callback=self.parse_photo)
        #'''

        yield photo