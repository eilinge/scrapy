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
from Boss.items import BossItem
from Boss.settings import USER_AGENT
from scrapy.linkextractors import LinkExtractor

chrome_options = Options()
driver = webdriver.Chrome()

class BossSpider(scrapy.Spider):
    name = 'boss'
    allowed_domains = ['www.zhipin.com']
    start_urls = ['http://www.zhipin.com/']

    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        'Content-Length': '11',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Host': 'www.zhipin.com',
        'Origin': 'www.zhipin.com',
        'Referer': 'http://www.zhipin.com/',
        'User-Agent': USER_AGENT,
        'X-Requested-With': 'XMLHttpRequest',
    }

    def start_requests(self):
        driver.get(
            self.start_urls[0]
            )
        time.sleep(3)

        #搜索python爬虫
        driver.find_element_by_name('query').send_keys(u'python爬虫')
        time.sleep(3)
        driver.find_element_by_class_name('btn-search').click()
        time.sleep(3)

        new_url = driver.current_url.encode('utf8') #获取跳转之后的url
        yield scrapy.Request(new_url)

    def parse(self, response):
        #提取网页链接url
        links = LinkExtractor(restrict_css="div.info-primary>h3>a")
        link = links.extract_links(response)
        for each_link in link:
            yield scrapy.Request(each_link.url,callback=self.job_detail)


    def job_detail(self,response):
        spiderItem = BossItem()
        #想要提取的信息
        spiderItem['job_title']     = response.css('div.job-primary.detail-box div.name h1::text').extract()[0]
        spiderItem['salary']        = response.css('div.job-primary.detail-box span.badge ::text').extract()[0]
        spiderItem['address']       = response.css('div.job-primary.detail-box p::text').extract()[0]
        spiderItem['job_time']      = response.css('div.job-primary.detail-box p::text').extract()[1]
        spiderItem['education']     = response.css('div.job-primary.detail-box p::text').extract()[2]
        spiderItem['company']       = response.css('div.job-primary.detail-box div.info-company h3.name a::text').extract()[0]
        spiderItem['company_info']  = response.css('div.job-primary.detail-box div.info-company>p::text').extract()[0]

        detail = response.css('div.job-sec div.text ::text').extract()
        details = ''.join(detail)      #将列表内所有字符串提取成一个整的字符串
        spiderItem['detail_text']   = details

        print spiderItem
        yield spiderItem