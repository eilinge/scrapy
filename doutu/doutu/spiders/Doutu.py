# -*- coding: utf-8 -*-
import scrapy
from doutu.items import DoutuItem
from scrapy.linkextractors import LinkExtractor
import pdb

class DoutuSpider(scrapy.Spider):
    name = 'Doutu'
    #allowed_domains = ['www.doutula.com']
    start_urls = ['http://www.doutula.com/']

    def parse(self, response):
        #doutu = DoutuItem()
        #pdb.set_trace()

        le = LinkExtractor(restrict_css='div.col-sm-9')
        links = le.extract_links(response)
        for link in links[1:4]:
            yield scrapy.Request(link.url,callback=self.parse_pager)


        le1 = LinkExtractor(restrict_css='ul.pagination')
        links1 = le1.extract_links(response)
        for link1 in links1:
            yield scrapy.Request(link1.url,callback=self.parse)

        #pass

    def parse_pager(self,response):
        #pdb.set_trace()
        le2 = LinkExtractor(restrict_css='div.pic-content')
        links2 = le2.extract_links(response)
        for link2 in links2:
            yield scrapy.Request(link2.url,callback=self.parse_img)

    def parse_img(self,response):

        doutu = DoutuItem()

        doutu['image_urls'] = response.xpath('//div[@class="swiper-slide"]//img/@src').extract()[0]

        yield doutu

        #return doutu



