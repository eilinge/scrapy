# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request,FormRequest
import json
from PIL import Image
from io import BytesIO,StringIO
import pytesseract
from scrapy.log import logger
from douban.settings import USER_AGENT
import pdb
import urllib
from douban.items import DoubanItem
#from WebPImagePlugin


class LoginSpider(scrapy.Spider):
    name = 'login'
    allowed_domains = ['www.douban.com']
    start_urls = ['https://www.douban.com/']

    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'Connection': 'keep-alive',
        'Content-Length': '11',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Host': 'www.douban.com',
        'Origin': 'www.douban.com',
        'Referer': 'https://www.douban.com/',
        'User-Agent': USER_AGENT,
        'X-Requested-With': 'XMLHttpRequest',
    }

    def parse(self, response):
        pass

    #pdb.set_trace()
    login_url = 'http://www.douban.com'
    user = 'sssxxx'
    password = 'xxxx'

    def start_requests(self):
        yield Request(self.login_url,callback=self.login,dont_filter=True)

    def login(self,response):
        login_response = response.meta.get('login_response')

        '''
        pdb.set_trace()
        img_url = DoubanItem()
        img_url['image_urls'] = response.css('div.item.item-captcha img::attr(src)').extract()[0].encode('utf8')+"./captcha.jpg"
        yield img_url
        '''
        #pdb.set_trace()
        #img_url  = response.css('div.item.item-captcha img::attr(src)').extract()[0].encode('utf8')# + "./captcha.jpg"

        pdb.set_trace()
        img_url = 'https://www.douban.com/misc/captcha?id=U446rXuWcvTqx90816pmVAOC:en&size=s'
        img_url1 = urllib.urlretrieve(img_url, filename="./captcha.jpg")
        #img_url = r'C:\Users\wuchan4x\Desktop\StudyForIntel\beauty\full\00d43c7a93cc6e6f1ce2c6cac2b3f80d9f5ed5c9.jpg'
        #img_url = r'C:\Users\wuchan4x\Desktop\Capture.PNG'

        if not login_response:
            captchaUrl = response.css('label.field.prepend-icon ::attr(src)').extract()
            captchaUrl = response.urljoin(captchaUrl)

            yield Request(captchaUrl,
                          callback=self.login,
                          meta={'login_response':response},
                          dont_filter=True)

        else:
            formdata1 = {
                'email':self.user,
                'pass' :self.password,
                #'code' :self.get_captcha_by_OCR(response.body)
                'code': self.get_captcha_by_OCR(img_url1)
            }

            yield FormRequest.from_response(login_response,
                                        callback=self.parse_login,
                                        formdata=formdata1,
                                        dont_filter=True)

    def parse_login(self,response):
        #pdb.set_trace()
        info = json.loads(response.text)
        if info['error'] == '0':
            logger.info('ok')
            return super().start_requests()
        logger.info('failed')
        return self.start_requests()

    def get_captcha_by_OCR(self,data):
        #pdb.set_trace()
        #img = Image.open(BytesIO(data))
        #img = Image.open(StringIO(data))
        img = Image.open(data[0])
        img = img.convert('L')
        captcha = pytesseract.image_to_string(img)
        img.close()

        return captcha
    
