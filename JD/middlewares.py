# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html

import random  
import scrapy  
from scrapy import log
import json
  
  
# logger = logging.getLogger()  
  
class ProxyMiddleware(object):  
    """docstring for ProxyMiddleWare"""  
    def process_request(self,request, spider):  
        '''对request对象加上proxy'''  
        proxy = self.get_random_proxy()  
        print("this is request ip:"+ proxy)  
        request.meta['proxy'] = proxy
  
  
    def process_response(self, request, response, spider):  
        '''对返回的response处理'''  
        # 如果返回的response状态不是200，重新生成当前request对象  
        if response.status != 200:  
            proxy = self.get_random_proxy()  
            print("this is response ip:"+proxy)  
            # 对当前request加上代理  
            request.meta['proxy'] = proxy   
            return request  
        return response  
  
    def get_random_proxy(self):  
        '''随机从文件中读取proxy'''  
        with open('JD/ip_pool/ip_pool.txt', 'r') as f:
            ip_list = json.load(f)  
        ip = random.choice(ip_list)
        for key in ip.keys():
            protocol = key
        proxy = protocol + '://' + ip[protocol]
        return proxy  

