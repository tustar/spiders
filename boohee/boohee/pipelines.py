# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import sqlite3
from boohee.items import CategoryItem, FoodItem


class BooheePipeline(object):

    def __init__(self):
        self.conn = None
        self.filename = "boohee.db"

    def process_item(self, item, spider):
        if item.__class__ == CategoryItem:
            values = [(item["group_type"], item["name"], item[
                "thumb_img_url"], item["group_url"])]
            cursor = self.conn.cursor()
            cursor.executemany(
                """insert into category ("group_type", "name", "thumb_img_url", "group_url") values(?,?,?,?);""",
                values)
        elif item.__class__ == FoodItem:
            values = [(item["category_id"], item["calory"], item[
                "weight"], item["code"], item["name"], item["name_en"], item["name_hk"])]
            cursor = self.conn.cursor()
            cursor.executemany(
                """insert into food ("category_id" , "calory", "weight", "code","name", "name_en","name_hk") values(?,?,?,?,?,?,?);""",
                values)
        return item

    def open_spider(self, spider):
        self.conn = self.create_table(self.filename)

    def close_spider(self, spider):
        if self.conn:
            self.conn.commit()
            self.conn.close()
            self.conn = None

    @staticmethod
    def create_table(filename):
        conn = sqlite3.connect(filename)
        cursor = conn.cursor()
        # category
        cursor.execute("""DROP TABLE IF EXISTS "category";""")
        cursor.execute("""CREATE TABLE "category" (
            "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            "group_type" TEXT NOT NULL,
            "name" TEXT NOT NULL,
            "thumb_img_url" TEXT NOT NULL,
             "group_url" TEXT NOT NULL
        );""")
        # food
        cursor.execute("""DROP TABLE IF EXISTS "food";""")
        cursor.execute("""CREATE TABLE "food" (
                "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                "category_id" INTEGER NOT NULL,
                "calory" REAL NOT NULL,
                "weight" REAL NOT NULL,
                "code" TEXT NOT NULL,
                "name" TEXT NOT NULL,
                "name_en" TEXT NOT NULL,
                "name_hk" TEXT NOT NULL
            );""")
        # commit
        conn.commit()
        return conn
