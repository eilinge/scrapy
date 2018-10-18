# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request,FormRequest
import pdb

class PachSpider(scrapy.Spider):                            #定义爬虫类，必须继承scrapy.Spider
    name = 'pach1'                                           #设置爬虫名称
    allowed_domains = ['edu.iqianyue.com']                  #爬取域名
    # start_urls = ['http://edu.iqianyue.com/index_user_login.html']     #爬取网址,只适于不需要登录的请求，因为没法设置cookie等信息

    header = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0'}  #设置浏览器用户代理

    def start_requests(self):
        #第一次请求页面时,开启cookie
        return [Request('http://edu.iqianyue.com/index_user_login.html',meta={'cookiejar':1},callback=self.parse)]

    def parse(self,response):

        formdata = {
            'name':'lalla',
            'passwd':'wcq159753?',
            'submit':'',
        }

        cookie1 = response.headers.getlist('Set-Cookie')  #['PHPSESSID=qlfaqpnnavesha2dm6h4kb6rn6; path=/']
        print(cookie1)
        print('loging')
        pdb.set_trace()
        return [FormRequest.from_response(response,
                                       url = 'http://edu.iqianyue.com/index_user_login',
                                       meta={'cookiejar':response.meta['cookiejar']},
                                       formdata= formdata,
                                       callback=self.next,)]

    def next(self,response):
        #pass
        a = response.body.decode('utf-8')
        pdb.set_trace()
        yield Request('http://edu.iqianyue.com/index_user_index.html',meta={'cookiejar':'True'},callback=self.next2)

    def next2(self,response):
        cookie2 = response.headers.getlist('Set-Cookie')   #['PHPSESSID=8i3dv6fn3265uldvvrrhr7qj72; path=/']
        print(cookie2)
        pdb.set_trace()
        body = response.body
        body1 = response.body_as_unicode()

        #a = response.xpath('div[@class="tab-pane active"]').extract()[0]
        a = response.xpath('/html/head/title/text()').extract()[0].encode('utf8')
        print(a)

