#!/usr/bin/env python
# -*- coding:utf-8 _*-
"""
@author:yiuman
@time: 2019/07/01

"""

import scrapy
import json
from urllib.parse import urlencode
from scrapy import Selector

from quaScrapy.items import AttractionsItem, EvaluationItem


class QuaSpider(scrapy.Spider):
    name = "qua"
    allowed_domains = ['piao.qunar.com']
    domain = 'https://piao.qunar.com'
    base_url = domain + '/ticket/list_{0}.html?keyword={0}&page={1}'

    def __init__(self, keywords=None, page=1, *args, **kwargs):
        super(QuaSpider, self).__init__(*args, **kwargs)
        self.page = page
        if keywords is None:
            self.keywords = ['阳山']
        else:
            self.keywords = keywords
        self.start_urls = [self.base_url.format(keyword, self.page) for keyword in self.keywords]

    def parse(self, response):
        responseSelector = Selector(response)
        for sel in responseSelector.xpath('//div[@class="sight_item"]'):
            item = AttractionsItem()
            item['id'] = sel.xpath('@data-id').extract_first()
            item['name'] = sel.xpath('.//h3[@class="sight_item_caption"]/a/text()').extract_first()
            item['price'] = sel.xpath('.//span[@class="sight_item_price"]/em/text()').extract_first()
            item['sales'] = sel.xpath('.//td[@class="sight_item_sold-num"]/span/text()').extract_first()
            item['heat'] = sel.xpath('.//span[@class="product_star_level"]/em/span/text()').extract_first()
            item['address'] = sel.xpath('.//p[@class="address color999"]/span/text()').extract_first()
            detail_url = sel.xpath('.//a[@class="sight_item_do"]/@href').extract_first()
            yield scrapy.Request(url=self.domain + detail_url, meta={'item': item},
                                 callback=self.parse_detail)

        # 判断是否有下一页按钮，有的话继续爬
        nextButton = responseSelector.xpath('//a[@class="next"]')
        if len(nextButton) > 0:
            url = response.url
            prefix = url[0:-1]
            page = int(url[-1]) + 1
            yield scrapy.Request(url=prefix + str(page), callback=self.parse)

    # 详情页面
    def parse_detail(self, response):
        item = response.meta['item']
        item['score'] = response \
            .xpath(
            '//div[@class="mp-description-comments"]/span[@id="mp-description-commentscore"]/span/text()') \
            .extract_first()
        sightId = response.xpath('//div[@id="mp-tickets"]/@data-sightid').extract_first()
        tags = [{'tagType': tagLabel.xpath('@data-type').extract_first(),
                 'tagCount': tagLabel.xpath('text()').re_first(r'[(](.*?)[)]'),
                 'tagName': tagLabel.xpath('text()').extract_first().split('(')[0]
                 }
                for tagLabel in response.xpath('//li[@mp-role="tagItem"]')
                if tagLabel.xpath('@data-type').extract_first() != '0']
        yield item

        # 爬取景点评论数据
        for tag in tags:
            params = {'sightId': sightId, 'index': '1', 'page': '1', 'pageSize': str(tag['tagCount']),
                      'tagType': str(tag['tagType'])}
            yield scrapy.Request(url=self.domain + '/ticket/detailLight/sightCommentList.json?' + urlencode(params),
                                 meta={'itemId': item['id'], 'type': str(tag['tagType']), 'text': str(tag['tagName'])},
                                 callback=self.parse_evaluations)

    # 爬取景点评论数据
    def parse_evaluations(self, response):
        itemId = response.meta['itemId']
        evaluationType = response.meta['type']
        evaluationText = response.meta['text']
        if response.body:
            load = json.loads(response.body)
            for evaluation in load['data']['commentList']:
                evaluationItem = EvaluationItem()
                evaluationItem['id'] = evaluation['commentId']
                evaluationItem['itemId'] = itemId
                evaluationItem['evaluationType'] = evaluationType
                evaluationItem['evaluationText'] = evaluationText
                evaluationItem['author'] = evaluation['author']
                evaluationItem['content'] = evaluation['content']
                evaluationItem['createDate'] = evaluation['date']
                evaluationItem['score'] = evaluation['score']
                evaluationItem['imgs'] = json.dumps(evaluation['imgs'])
                evaluationItem['userNickName'] = evaluation['userNickName']
                yield evaluationItem
