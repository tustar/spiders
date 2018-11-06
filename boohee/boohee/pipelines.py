# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
import pymysql.cursors
import logging
from twisted.enterprise import adbapi
from boohee.items import CategoryItem, FoodItem


class BooheePipeline(object):

    def __init__(self, dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls, settings):
        args = dict(
            host=settings['MYSQL_HOST'],
            db=settings['MYSQL_DBNAME'],
            user=settings['MYSQL_USER'],
            passwd=settings['MYSQL_PASSWD'],
            charset='utf8',
            cursorclass=pymysql.cursors.DictCursor,
            use_unicode=True)

        dbpool = adbapi.ConnectionPool("pymysql", **args)
        return cls(dbpool)

    def process_item(self, item, spider):
        logging.debug(item)
        query = self.dbpool.runInteraction(self.insert, item)
        query.addErrback(self.handler_error)
        return item

    def open_spider(self, spider):
        query = self.dbpool.runInteraction(self.create_table)
        query.addErrback(self.handler_error)

    def close_spider(self, spider):
        self.dbpool.close()

    @staticmethod
    def handler_error(error):
        logging.error('Error-DB::CategoryItem %s' % repr(error))

    @staticmethod
    def insert(cursor, item):
        insert_sql, params = item.get_insert_sql()
        cursor.execute(insert_sql, params)

    @staticmethod
    def create_table(cursor):
        # category
        cursor.execute(CategoryItem.create_table)
        # food
        cursor.execute(FoodItem.create_table)
