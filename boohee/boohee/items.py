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

    create_table = """CREATE TABLE IF NOT EXISTS `category` (
                `id` INT NOT NULL AUTO_INCREMENT,
                `group_type` VARCHAR(50) NOT NULL UNIQUE,
                `name` TEXT NOT NULL,
                `thumb_img_url` TEXT NOT NULL,
                `group_url` TEXT NOT NULL,
                PRIMARY KEY ( `id` )
                )ENGINE=InnoDB DEFAULT CHARSET=utf8;"""

    def get_insert_sql(self):
        insert_sql = """INSERT INTO category (
            group_type, 
            name, 
            thumb_img_url, 
            group_url) 
            VALUES(%s,%s,%s,%s);"""
        params = (
            self['group_type'],
            self['name'],
            self['thumb_img_url'],
            self['group_url']
        )
        return insert_sql, params


class FoodItem(Item):
    category_id = Field()
    calory = Field()
    weight = Field()
    code = Field()
    name = Field()
    name_en = Field()
    name_hk = Field()
    thumb_img_url = Field()
    detail_url = Field()

    create_table = """CREATE TABLE IF NOT EXISTS `food` (
            `id` INT NOT NULL AUTO_INCREMENT,
            `category_id` INT NOT NULL,
            `calory` FLOAT NOT NULL,
            `weight` FLOAT NOT NULL,
            `code` VARCHAR(100) NOT NULL UNIQUE,
            `name` VARCHAR(400) NOT NULL UNIQUE,
            `name_en` TEXT NOT NULL,
            `name_hk` TEXT NOT NULL,
            `thumb_img_url` TEXT NOT NULL,
            `detail_url` TEXT NOT NULL,
            PRIMARY KEY ( `id` )
            )ENGINE=InnoDB DEFAULT CHARSET=utf8;"""

    def get_insert_sql(self):
        insert_sql = """INSERT INTO food (
            category_id , 
            calory, 
            weight, 
            code,
            name, 
            name_en, 
            name_hk, 
            thumb_img_url,
            detail_url) 
            VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s);"""
        params = (
            self['category_id'],
            self['calory'],
            self['weight'],
            self['code'],
            self['name'],
            self['name_en'],
            self['name_hk'],
            self['thumb_img_url'],
            self['detail_url']
        )
        return insert_sql, params
