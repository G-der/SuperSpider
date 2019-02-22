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


class ZhihuItem(scrapy.Item):
    """知乎"""
    collection = scrapy.Field()  # 表名
    question = scrapy.Field()
    username = scrapy.Field()
    userfans = scrapy.Field()
    user_url = scrapy.Field()
    ans__url = scrapy.Field()
    ans_detl = scrapy.Field()
    pushtime = scrapy.Field()
    follower = scrapy.Field()
    anscommt = scrapy.Field()
    update_datetime = scrapy.Field()  # 插入记录的时间


class TBItem(scrapy.Item):
    """淘宝"""
    keyword = scrapy.Field()
    title = scrapy.Field()
    commodity_url = scrapy.Field()
    price = scrapy.Field()
    volume = scrapy.Field()
    shop_name = scrapy.Field()
    shop_url = scrapy.Field()
    shop_location = scrapy.Field()









