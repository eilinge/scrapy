# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BossItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    #pass
    job_title = scrapy.Field()
    salary    = scrapy.Field()
    address   = scrapy.Field()
    job_time  = scrapy.Field()
    education = scrapy.Field()
    company   = scrapy.Field()
    company_info= scrapy.Field()
    detail_text = scrapy.Field()