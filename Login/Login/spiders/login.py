# -*- coding: utf-8 -*-
import scrapy
import json
from scrapy.selector import Selector
from scrapy import FormRequest,Request
import pdb
from Login.settings import USER_AGENT
import time
from PIL import Image
import urllib
import re

class ExampleLoginSpider(scrapy.Spider):
    name = "login"


    allowed_domains = ["example.webscraping.com"]
    #start_urls = ['http://example.webscraping.com/user/profile']
    login_url = 'http://example.webscraping.com/places/default/user/login'
    #login_url = 'https://github.com/login'
    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        'Content-Length': '11',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        # 'Host': 'matplotlib.org',
        # 'Origin': 'matplotlib.org',
        'Referer': 'http://example.webscraping.com/places/default/user/login',
        'User-Agent': USER_AGENT,
        'X-Requested-With': 'XMLHttpRequest',
    }

    # 网页主页
    #def parse(self, response):
        #print(response.text)

    def start_requests(self):
        #pdb.set_trace()
        #为了能使用同一个状态持续的爬取网站, 就需要保存cookie, 使用cookie保存状态,
        yield scrapy.Request(self.login_url,meta={'cookiejar':1},callback=self.parse_login) #启用cookie
    def parse_login(self,response):
        #pdb.set_trace()
        next = response.xpath('//input[@name="_next"]/@value').extract()[0]
        formname = response.xpath('//input[@name="_formname"]/@value').extract()[0]
        formkey = response.xpath('//input[@name="_formkey"]/@value').extract()[0]
        formdata = {'email':'17601329166@163.com',
                    'password':'wcq159753?',
                    '_next':next,
                    '_formkey':formkey,
                    '_formname':formname,
                    }

        yield FormRequest.from_response(response,formdata=formdata,meta={'cookiejar':response.meta['cookiejar']},#注意这里cookie的获取
                                        callback=self.parse_after)

    def parse_after(self,response):
        pdb.set_trace()
        if 'Welcome' in response.body:
            print 'login acuessfully'
