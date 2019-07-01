#!/usr/bin/env python
# -*- coding:utf-8 _*-
"""
@author:yiuman
@time: 2019/07/01

"""

import scrapy


# 去哪儿景点信息
class AttractionsItem(scrapy.Item):
    id = scrapy.Field()
    name = scrapy.Field()
    price = scrapy.Field()
    sales = scrapy.Field()
    heat = scrapy.Field()
    address = scrapy.Field()
    score = scrapy.Field()


# 景点评论
class EvaluationItem(scrapy.Item):
    id = scrapy.Field()
    itemId = scrapy.Field()
    evaluationType = scrapy.Field()
    evaluationText = scrapy.Field()
    author = scrapy.Field()
    content = scrapy.Field()
    createDate = scrapy.Field()
    score = scrapy.Field()
    imgs = scrapy.Field()
    userNickName = scrapy.Field()
