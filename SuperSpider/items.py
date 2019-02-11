# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class SuperspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class BaseItem(scrapy.Item):
    title = scrapy.Field()  # 标题
    collection = scrapy.Field()  # 表名
    username = scrapy.Field()  # 用户名
    usergender = scrapy.Field()  # 用户性别
    userlocation = scrapy.Field()  # 用户所在地
    push_time = scrapy.Field()  # 发表时间
    comment_detail = scrapy.Field()  # 评论详情
    comment_url = scrapy.Field()  # 评论网址
    catch_time = scrapy.Field()  # 抓取时间
    data_from = scrapy.Field()  # 数据来源





