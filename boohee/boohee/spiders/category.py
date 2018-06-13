# -*- coding: utf-8 -*-
from scrapy.spiders import Spider
from scrapy.selector import Selector
from boohee.items import CategoryItem, FoodItem
from scrapy.http import Request
import re


class CategorySpider(Spider):
    name = 'category'
    allowed_domains = ['boohee.com']
    SERVER_URL = "http://www.boohee.com"
    start_urls = ['{}/food'.format(SERVER_URL)]

    def parse(self, response):
        self.log('A response from %s just arrived!' % response.url)
        values = response.xpath('//div[@id="main"]//li')
        categorys = []

        for value in values:
            item = CategoryItem()
            group_url = value.xpath(
                'div[@class="img-box"]//a/@href').extract_first().strip()
            item['group_url'] = "{}{}".format(self.SERVER_URL, group_url)
            item['group_type'] = group_url.split('/')[-1]
            item['thumb_img_url'] = value.xpath(
                'div[@class="img-box"]//a//img/@src').extract_first().strip()
            item['name'] = value.xpath(
                'div[@class="text-box"]//h3//a/text()').extract_first().strip()
            categorys.append(item)
            yield item

        for index, value in enumerate(categorys):
            category = categorys[index]
            yield Request(category['group_url'], meta={"category_id": index + 1}, callback=self.parse_food)

    def parse_food(self, response):
        self.log('A response from %s just arrived!' % response.url)
        category_id = response.meta["category_id"]
        values = response.xpath('//ul[@class="food-list"]//li')
        for value in values:
            item = FoodItem()
            item['category_id'] = category_id
            detail_url = value.xpath(
                'div[@class="img-box pull-left"]//a/@href').extract_first().strip()
            item['detail_url'] = "{}{}".format(self.SERVER_URL, detail_url)
            item['code'] = detail_url.split('/')[-1]
            item['thumb_img_url'] = value.xpath(
                'div[@class="img-box pull-left"]//a//img/@src').extract_first().strip()
            item['name'] = value.xpath(
                'div[@class="text-box pull-left"]//h4//a/text()').extract_first().strip()
            calory_weight = value.xpath(
                'div[@class="text-box pull-left"]//p/text()').extract_first().strip()
            temp = calory_weight.split(' ')
            item['calory'] = re.sub("\D",  "", str(temp[0])) 
            item['weight'] = re.sub("\D", "", str(temp[-1])) 
            yield item

        next_page = response.xpath(
            '//div[@class="pagination"]//a[@class="next_page"]/@href').extract_first()
        next_page = "{}{}".format(self.SERVER_URL, next_page)
        yield Request(next_page, meta={"category_id": category_id}, callback=self.parse_food)
