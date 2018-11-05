# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field


class CategoryItem(Item):
    group_type = Field()
    group_url = Field()
    name = Field()
    thumb_img_url = Field()


class FoodItem(Item):
    category_id = Field()
    calory = Field()
    weight = Field()
    code = Field()
    name = Field()
    name_en = Field()
    name_hk = Field()
