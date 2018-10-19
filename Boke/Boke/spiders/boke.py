#-*- coding:utf-8 -*-
import time
from selenium import webdriver
import pdb
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys    import Keys
from lxml import etree
import re
from bs4 import BeautifulSoup
import scrapy
from Boke.items import BokeItem
from Boke.settings import USER_AGENT
from scrapy.linkextractors import LinkExtractor
import random
import re


chrome_options = Options()
driver = webdriver.Chrome()

class BokeSpider(scrapy.Spider):
    name = 'boke'
    allowed_domains = ['www.cnblogs.com','passport.cnblogs.com']
    start_urls = ['https://passport.cnblogs.com/user/signin']

    def start_requests(self):

        driver.get(
            self.start_urls[0]
            )
        time.sleep(3)
        driver.find_element_by_id('input1').send_keys(u'eilinge')
        time.sleep(3)
        driver.find_element_by_id('input2').send_keys(u'wcq159753?')
        time.sleep(3)
        driver.find_element_by_id('signin').click()
        time.sleep(20)

        new_url = driver.current_url.encode('utf8')
        print(driver.current_url.encode('utf8'))

        yield scrapy.Request(new_url)

    def parse(self, response):

        bokeitem = BokeItem()
        sels = response.css('div.day')
        for sel in sels:
            #pdb.set_trace()
            bokeitem['name'] = sel.css('div.postTitle>a ::text').extract()[0]
            bokeitem['summary'] = sel.css('div.c_b_p_desc ::text').extract()[0]
            summary = sel.css('div.postDesc ::text').extract()[0]
            bokeitem['read_num'] = re.findall(r'\((\d{0,5})',summary)[0]
            bokeitem['comment'] = re.findall(r'\((\d{0,5})', summary)[1]

            print bokeitem
            yield bokeitem