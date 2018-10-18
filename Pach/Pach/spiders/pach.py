# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request,FormRequest
from Pach.settings import USER_AGENT
import pdb

class PachSpider(scrapy.Spider):                            #定义爬虫类，必须继承scrapy.Spider
    name = 'pach'                                           #设置爬虫名称
    allowed_domains = ['edu.iqianyue.com']                  #爬取域名
    # start_urls = ['http://edu.iqianyue.com/index_user_login.html']     #爬取网址,只适于不需要登录的请求，因为没法设置cookie等信息

    header = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0'}  #设置浏览器用户代理
    '''
    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'Connection': 'keep-alive',
        'Content-Length': '11',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Host': 'edu.iqianyue.com',
        'Origin': 'edu.iqianyue.com',
        #'Referer': 'http://www.dy2018.com/html/tv/oumeitv/index.html',
        'User-Agent': USER_AGENT,
        'X-Requested-With': 'XMLHttpRequest',

    }
    '''

    def start_requests(self):       #用start_requests()方法,代替start_urls
        """第一次请求一下登录页面，设置开启cookie使其得到cookie，设置回调函数"""
        yield Request('http://edu.iqianyue.com/index_user_login.html',meta={'cookiejar':1},callback=self.parse)

    def parse(self, response):      #parse回调函数

        data =  {                    #设置用户登录信息，对应抓包得到字段
            'number':'17601329166',
            'passwd':'wcq159753?',
            'submit':''
                }
        # 响应Cookie
        Cookie1 = response.headers.getlist('Set-Cookie')   #查看一下响应Cookie，也就是第一次访问注册页面时后台写入浏览器的Cookie
        print('cookie1',Cookie1)
        #pdb.set_trace()
        #print('登录中')
        """第二次用表单post请求，携带Cookie、浏览器代理、用户登录信息，进行登录给Cookie授权"""
        yield FormRequest.from_response(response,
                                          url='http://edu.iqianyue.com/index_user_login.html',   #真实post地址
                                          meta={'cookiejar':response.meta['cookiejar']},
                                          headers=self.header,
                                          formdata=data,
                                          callback=self.next,
                                        )
    def next(self,response):
        #a = response.body.decode("utf-8")   #登录后可以查看一下登录响应信息
        #pdb.set_trace()
        #print(a)
        """登录后请求需要登录才能查看的页面，如个人中心，携带授权后的Cookie请求"""
        yield Request('http://edu.iqianyue.com/index_user_index.html',meta={'cookiejar':True},callback=self.next2)

    def next2(self,response):
        # 请求Cookie
        #pdb.set_trace()
        #Cookie2 = response.request.headers.getlist('Cookie')
        #print(Cookie2)
        body = response.body  # 获取网页内容字节类型
        unicode_body = response.body_as_unicode()  # 获取网站内容字符串类型
        a = response.css('div.col-md-4.column ::text').extract()[2]
        #a = response.css('div#panel-54098 h2::text').extract()  #得到个人中心页面
        print(a)