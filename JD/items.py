# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ProductItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    product_id = scrapy.Field()
    product_rank = scrapy.Field()
    product_name = scrapy.Field() #配置？？？
    product_price = scrapy.Field()
    product_store = scrapy.Field()
    comment_num = scrapy.Field()# 总的评论数量
    comment_rate = scrapy.Field()# 好评率
    comment_detail = scrapy.Field() # 具体评论：姓名/等级/内容/星级/时间

