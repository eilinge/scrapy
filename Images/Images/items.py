# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ImagesItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    #pass
    images_url = scrapy.Field()
    imges      = scrapy.Field()
