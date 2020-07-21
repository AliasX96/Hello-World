# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class XiechengItem(scrapy.Item):
    note_time = scrapy.Field() #游记时间
    title = scrapy.Field() #标题
    user = scrapy.Field() #作者
    user_gender = scrapy.Field()#作者性别
    days = scrapy.Field() #天数
    travel_time = scrapy.Field() #旅游时间
    per_capital_spending = scrapy.Field() #人均花销
    with_whom = scrapy.Field() #和谁一起
    plays = scrapy.Field() #玩法
    liked = scrapy.Field() #游记喜欢数
    comments = scrapy.Field() #游记评论数
    views = scrapy.Field() #游记浏览数
    # content = scrapy.Field() #游记内容
    link = scrapy.Field() #游记链接
    pass
