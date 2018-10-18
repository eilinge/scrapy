# -*- coding: utf-8 -*-
import scrapy
import pdb
from Books.settings import USER_AGENT
from Books.items    import BooksItem
from scrapy.linkextractors import LinkExtractor

class BooksSpider(scrapy.Spider):
    name = 'books'
    #allowed_domains = ['books.toscrape.com']
    start_urls = ['http://books.toscrape.com']
    #start_urls = ['https://blog.csdn.net/u011781521/article/details/70194744?locationNum=4&fps=1']

    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        'Content-Length': '11',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Host': 'books.toscrape.com',
        'Origin': 'books.toscrape.com',
        'Referer': 'http://books.toscrape.com',
        'User-Agent': USER_AGENT,
        'X-Requested-With': 'XMLHttpRequest',
    }

    def parse(self, response):
        #pass
        sels = response.css('article.product_pod')
        book = BooksItem()
        for sel in  sels:

            book['name'] = sel.css('h3 a::attr(title)').extract()[0]
            book['price'] = sel.css('div.product_price p::text').extract()[0]

            yield book
            #yield{ 'name':name,
                   #'price':price}
        links = LinkExtractor(restrict_css='ul.pager li.next')
        link = links.extract_links(response)
        yield scrapy.Request(link[0].url,callback=self.parse)
