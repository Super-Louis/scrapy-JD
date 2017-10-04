# -*- coding: utf-8 -*-
import scrapy
import re
import requests
import json
import threading
from JD.items import ProductItem
import time
from JD.ip_pool.get import get_response
import pymongo

class JDSpider(scrapy.Spider):
	name = 'JD'
	allowed_domains = ['jd.com']
	client = pymongo.MongoClient()
	# 与数据库连接，避免重复爬取
	db = client['items']
	collection = db['JD_Laptop']
	# brand: * ; price: 3900-5199; sort: sales; limit:top 60(first page)
	# start_urls默认情况下是一个集合
	start_urls = ['https://list.jd.com/list.html?cat=670,671,672&ev=exprice_M3900L5199&sort=sort_totalsales15_desc&trans=1']
	head = {'cache-control':'no-cache',
			'referer':'https://list.jd.com/list.html',
			'user-agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
			'cookie':'TrackID=19blJPNAMy9IZ6uZD45obrfQCL8shz225pBx82yXjPmtEReUnEXVQWmJ9ht4ejKGKXniSX_u8x4mgiYLd3_RQ_zGSXqxkNYV-r14ajOdAhkKqZocVPzSetohDOiOswX60; pinId=NeqIDosPOyzrcoIviREEErV9-x-f3wj7; unpl=V2_ZzNtbRACEBZwCxVdfU1YBWIBFFURUEQdcQ8TU3kRWAVnB0FbclRCFXMUR1xnGFQUZwUZWUdcRxZFCEdkeRpbAGcKF1lDZ3MURQtGZHMpXAFhBhBUS1VCEkU4T11LKR9dNVpGHkNXQiVwAEBUehhcAmAzE21KVEQTfQ9EUH4pF2tmThJZRFJBHHwKR1NLGGwG; __jdv=122270672|jcad.c-psa.net|t_326418450_|uniongoubiao|cdb242b87e514379b66956d6395115b7|1504950893802; ipLoc-djd=1-72-4137-0; areaId=1; __jda=122270672.1574388306.1504950891.1505093223.1505117715.5; __jdb=122270672.3.1574388306|5.1505117715; __jdc=122270672; __jdu=1574388306; 3AB9D23F7A4B3C9B=YCOJ4PP323YLTDHQWD5SRUZSPVUROSKTDPG6JRTSGSXA3RAGFXXLZYCD4XLEYTGM7YTBQ4S5VHXX7HB7H5PX64II3U'
			}
	# 用于存储comment

	#response没有指明回调函数时，默认使用该函数
	def parse(self, response): 
		tail_urls = response.xpath('//li[@class="gl-item"]//div[@class="p-name"]/a/@href').extract()
		rank = 0
		for tail_url in tail_urls:
			rank += 1
			url = "https:" + tail_url
			id = re.findall(r'/(\d+).html', url)[0]
			# print(url)
			# if self.collection.find_one({"product_id":id}): #不要掉了self!!!
			# 	print("该产品已存在")
			# else:
			exists = self.collection.find_one({"product_id":id})
			if exists and int(exists['comment_num']) <= len(exists['comment_detail']):
				print("该产品评论已加载")
			else:
				yield scrapy.Request(url, meta={'rank': rank}, callback=self.parse_product)

	def parse_product(self, response):
		#findall返回一个列表！即时只有一个元素！！！
		item = ProductItem()
		id = re.findall(r'/(\d+).html', response.url)[0]
		rank = response.meta['rank']
		name = response.xpath('//div[@class="sku-name"]/text()').extract()[0].strip()
		# 通过抓包分析，查看可疑js文件（含有price）， 得到实际价格请求，通过尝试删除多余项，简化url
		price_url = 'https://p.3.cn/prices/mgets?skuIds=J_' + str(id)
		price_page = requests.get(price_url, headers = self.head).text
		price = json.loads(price_page)[0]['p']
		store = response.xpath('//div[@class="J-hove-wrap EDropdown fr"]/div[@class="item"]/div/a/text()').extract()[0]
		# 每页十个评论（pagesize=10）,按照时间顺序排序（sortType=6）
		comment_url = 'https://club.jd.com/comment/skuProductPageComments.action?productId=%s&score=0&sortType=6&page=0&pageSize=10&isShadowSku=0&fold=1' % (id, )
		comment_json = requests.get(comment_url, headers=self.head).text
		comment_rate = json.loads(comment_json)["productCommentSummary"]["goodRateShow"]
		comment_num = json.loads(comment_json)["productCommentSummary"]['commentCount']
		flag = True
		# 粗略估计页面数
		page = int(comment_num)/10 + 10
		comment_details = []
		threads = []
		for i in range(0, int(page)):
			# 注意：当评论中有图片时，该评论会出现两次！
			comment_url = 'https://club.jd.com/comment/skuProductPageComments.action?productId=%s&score=0&sortType=6&page=%s&pageSize=10&isShadowSku=0&fold=1' % (id, str(i))
			# if comment_url in self.collection.find_one({'product_id':id})['comment_urls']:
			# 	print("该页评论已存在")
			# else:
			thread = threading.Thread(target=self.parse_comment, args=(comment_url, comment_details, id))
			threads.append(thread)
		for thread in threads:
			thread.start()
			time.sleep(2)
		for thread in threads:
			thread.join()
		#item的字段最好与返回的response中的字段相同，这样就可以通过循环给item赋值，以简化代码，在赋值前最好核实下response中是否存在该字段。
		# item = UserItem()
		# for field in item.fields:
  #   		if field in result.keys():
  #       	item[field] = result.get(field)
		# yield item
		item['product_id'] = id
		item['product_rank'] = rank
		item['product_name'] = name
		item['product_price'] = price
		item['product_store'] = store
		item['comment_num'] = comment_num
		item['comment_rate'] = comment_rate
		item['comment_detail'] = comment_details
		yield item

	def parse_comment(self, url, comment_details, id):
		s = requests.Session()
		s.headers = self.head
		response = get_response(s, url, proxy=True)
		# 将以爬取评论页面的url存入数据库, addToSet,避免重复插入！，push可能会插入重复值！！！
		# self.collection.update({'product_id':id}, {'$addToSet': {'comment_urls':url}})
		comment_list = json.loads(response.text)['comments']
		for comment in comment_list:
			comment_info = {}
			comment_info['user_id'] = comment['id']
			comment_info['nickname'] = comment['nickname']
			comment_info['userLevelName'] = comment['userLevelName']
			comment_info['userClientShow'] = comment['userClientShow']
			comment_info['creationTime'] = comment['creationTime']
			comment_info['days'] = comment['days']
			comment_info['score'] = comment['score']
			comment_info['content'] = comment['content']
			comment_details.append(comment_info)

			







