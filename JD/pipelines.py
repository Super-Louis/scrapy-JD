# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo
class JDPipeline(object):
	collection_name = 'JD_Laptop'
	def __init__(self, mongo_uri, mongo_db):
		self.mongo_uri = mongo_uri
		self.mongo_db = mongo_db

	@classmethod
	def from_crawler(cls, crawler):
		return cls(
			mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE', 'items'))

	def open_spider(self, spider):
		self.client = pymongo.MongoClient(self.mongo_uri)
		self.db = self.client[self.mongo_db]

	def close_spider(self,spider):
		self.client.close()

	def process_item(self, item, spider):
		if not self.db[self.collection_name].find_one({"product_id": item["product_id"]}):#注意一定要用find_one，否则没结果！！
			self.db[self.collection_name].insert(dict(item)) # dict(item)
		#改为大于等于！
		elif len(item['comment_detail']) >= len (self.db[self.collection_name].find_one({"product_id": item["product_id"]})['comment_detail']):
			self.db[self.collection_name].update({"product_id": item["product_id"]}, dict(item))
			return item

