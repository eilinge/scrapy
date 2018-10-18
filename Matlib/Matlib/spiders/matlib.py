# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from Matlib.items import MatlibItem
import pdb

class MatlibSpider(scrapy.Spider):
    name = 'matlib'
    allowed_domains = ['matplotlib.org']
    start_urls = ['https://matplotlib.org/examples/index.html']

    def parse(self, response):
        #le = LinkExtractor(restrict_css='div.toctree-wrapper.compound li.toctree-l2')
        le = LinkExtractor(restrict_css='div.toctree-wrapper.compound li.toctree-l1', deny='/index.html$')
        #pdb.set_trace()
        for link in le.extract_links(response):
            #print link.url
            yield scrapy.Request(link.url,callback=self.parse_url)
        #pass

    def parse_url(self,response):
        sel = response.css('a.reference.external::attr(href)').extract()[0]
        url = response.urljoin(sel)
        mpl = MatlibItem()
        #mpl['files_url'] = [url]
        #pdb.set_trace()
        mpl['files_url'] = url.encode('utf-8')
        #return mpl
        yield mpl

        #pass
