# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from dbmeinv.items import DbmeinvItem
import re
import pdb


class DbmeinvSpider(scrapy.Spider):
    name = 'Dbmeinv'
    allowed_domains = ['www.dbmeinv.com']
    #start_urls = ['http://www.dbmeinv.com/']
    start_urls = ['https://www.dbmeinv.com/index.htm?cid=6',
                  'https://www.dbmeinv.com/index.htm?cid=7',
                  'https://www.dbmeinv.com/index.htm?cid=3']

    def parse(self, response):
        le = LinkExtractor(restrict_css='ul.thumbnails')

        for link in le.extract_links(response):
            yield scrapy.Request(link.url,callback=self.parse_images)

        le1 = LinkExtractor(restrict_css='li.next_page')
        link1 = le1.extract_links(response)
        #pdb.set_trace()

        if link1:
            yield scrapy.Request(link1[0].url,callback=self.parse)

        #pass

    def parse_images(self,response):
        #pdb.set_trace()
        meinv = DbmeinvItem()
        #pdb.set_trace()

        #url1 = response.xpath('//div[@class="image-wrapper"]/img/@src').extract()[0]
        #url2 = response.xpath('//div[@class="topic-figure cc"]/img/@src').extract()[0]

        if response.xpath('//div[@class="image-wrapper"]/img/@src').extract():
            url1 = response.xpath('//div[@class="image-wrapper"]/img/@src').extract()[0]
            meinv['images_url'] = url1
            image_name = re.findall(r'large/(.+?\.jpg)',url1)
            meinv['images'] = image_name[0]

        if response.xpath('//div[@class="panel-body markdown"]//img/@src'):
            #url2 = response.xpath('//div[@class="topic-figure cc"]/img/@src').extract()[0]
            url2 = response.xpath('//div[@class="panel-body markdown"]//img/@src').extract()[0]
            meinv['images_url'] = url2
            image_name = re.findall(r'large/(.+?\.jpg)', url2)
            meinv['images'] = image_name[0]

        if response.xpath('//div[@class="topic-detail panel panel-default"]//img/@src'):
            url3 = response.xpath('//div[@class="topic-detail panel panel-default"]//img/@src').extract()[1]
            meinv['images_url'] = url3
            image_name = re.findall(r'large/(.+?\.jpg)', url3)
            meinv['images'] = image_name[0]

        yield meinv
'''
        else:
            url3 = response.xpath('//div[@class="topic-detail panel panel-default"]//img/@src').extract()[1]
            meinv['images_url'] = url3
            image_name = re.findall(r'large/(.+?\.jpg)', url3)
            meinv['images']    = image_name[0]
'''
