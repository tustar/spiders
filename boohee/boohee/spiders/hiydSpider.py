# -*- coding: utf-8 -*-
import re

from scrapy.http import Request
from scrapy.spiders import Spider

from boohee.items import CategoryItem, FoodItem
from boohee.util.translate import *


class Spider(Spider):
    name = 'hidy'
    allowed_domains = ['hiyd.com']
    SERVER_URL = "https://food.hiyd.com/"
    start_urls = [SERVER_URL]
    categorys = []

    def __init__(self, total=0):
        self._total = total

    @property
    def total(self):
        return self._total

    @total.setter
    def total(self, value):
        self._total = value

    def parse(self, response):
        self.log('A response from %s just arrived!' % response.url)

        yield from self.crawl_category(response)
        yield from self.crawl_food()

    def crawl_category(self, response):
        values = response.xpath('//div[@class="box box-main"]//ul//li//a')
        for value in values:
            item = CategoryItem()
            group_url = value.xpath('@href').extract_first().strip()
            item['group_url'] = "{}{}".format("https:", group_url)
            item['group_type'] = 11 + int(re.sub("\D", "", group_url.split('/')[-1]))
            item['thumb_img_url'] = value.xpath('div[@class="img-wrap"]//img/@src').extract_first().strip()
            item['name'] = value.xpath('h3[@class="group_name"]/text()').extract_first().strip()
            self.categorys.append(item)
            yield item

    def crawl_total(self):
        for _, value in enumerate(self.categorys):
            yield Request(value['group_url'], meta={"category_name": value['name']}, callback=self.parse_total)

    def crawl_food(self):
        for index, value in enumerate(self.categorys):
            yield Request(value['group_url'], meta={"category_id": index + 1}, callback=self.parse_food)

    def parse_total(self, response):
        self.log('A response from %s just arrived!' % response.url)
        category_name = response.meta["category_name"]
        ins = response.xpath('//div[@class="mod-page"]//ins//span//text()').extract_first()
        category_total = int(re.sub("\D", "", ins))
        logging.debug('%s: %d页 %d条', category_name, category_total, category_total * 20)
        self.total += category_total
        logging.debug('total: %d页 %d条', self.total, self.total * 20)

    def parse_food(self, response):
        self.log('A response from %s just arrived!' % response.url)
        category_id = response.meta["category_id"]
        values = response.xpath('//div[@class="list-main"]//li//a')
        self.log('items: %d' % len(values))
        for index, value in enumerate(values):
            item = FoodItem()
            try:
                item['category_id'] = category_id
                detail_url = value.xpath('@href').extract_first().strip()
                item['detail_url'] = "{}{}".format("https:", detail_url)
                item['code'] = detail_url.split('/')[-1].replace('detail-', '').replace('.html', '')
                item['thumb_img_url'] = value.xpath('div[@class="img-wrap"]//img/@src').extract_first().strip()
                name = value.xpath('div[@class="cont"]//h3//text()').extract_first().strip()
                new_name = update_name(name)
                item['name'] = new_name
                calory_weight = value.xpath('div[@class="cont"]//p//text()').extract_first().strip()
                temp = calory_weight.split(' ')
                item['calory'] = re.sub("\D", "", str(temp[0]))
                item['weight'] = re.sub("\D", "", str(temp[-1]))
                item['name_en'] = ''
                item['name_hk'] = chs_to_cht(new_name)
                yield item
            except Exception as e:
                print('Error-Xpath::parse_food[index=%d]%s %s' % (index, response.url, e))
            finally:
                pass

        try:
            next_page = response.xpath('//div[@class="mod-page"]//a[@rel="next"]/@href').extract_first()
            if next_page is None:
                print('Done-Category::parse_food[category_id=%d]' % category_id)
                return
            next_page = "{}{}".format(self.SERVER_URL, next_page)
            yield Request(next_page, meta={"category_id": category_id}, callback=self.parse_food)
        except Exception as e:
            print('Done-Category::parse_food[category_id=%d] %s' % (category_id, e))
        finally:
            pass
