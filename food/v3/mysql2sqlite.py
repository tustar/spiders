#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import logging
import sqlite3
import zhconv
import pymysql
import pymysql.cursors

logging.basicConfig(level=logging.DEBUG,
                    format='%(levelname)s %(asctime)s %(filename)s %(funcName)s [line:%(lineno)d] %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')

DB_NAME = "food_v3.db"
MIGRATION_FILE_NAME = "food_db_migration_2_3.txt"
MIGRATION_FILE_NAME_CSV = "food_db_migration_2_3.csv"

def csv_to_sqlite():
    # open db
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    lines = []
    with open(MIGRATION_FILE_NAME) as f:
        for line in f.readlines():
            try:
                values = line.replace("'", "''").replace('\n', '').split(',', 3)
                category_id = values[0]
                calory = values[1]
                code = values[2]
                name = values[3]
                print(values)
                print("{}={}={}={}".format(category_id, calory, code, name))
                sql = "INSERT INTO food('category_id', 'calory', 'weight','code', 'name', 'name_en', 'name_hk') " \
                      "VALUES ('{}', '{}','{}', '{}','{}', '{}','{}');" \
                    .format(category_id, calory, 100, code, name, '', '')
                print(sql)
                cursor.execute(sql)
                lines.append(line)
            except sqlite3.IntegrityError as e:
                print(e)

    save_csv(MIGRATION_FILE_NAME_CSV, lines)

    # close db
    conn.commit()
    conn.close()


def mysql_to_csv():
    # Connect to the database
    conn = pymysql.connect(host='localhost',
                           user='root',
                           password='tustar',
                           db='calorie',
                           charset='utf8',
                           cursorclass=pymysql.cursors.DictCursor)
    lines = []
    try:
        with conn.cursor() as cursor:
            # Read a single record
            sql = "SELECT category_id, calory, code, name FROM food"
            cursor.execute(sql)
            items = cursor.fetchall()
            for item in items:
                line = '{},{},{},{}\n'.format(item['category_id'], item['calory'], item['code'],
                                              zhconv.convert(item['name'], 'zh-hans'))
                lines.append(line)
            save_csv(MIGRATION_FILE_NAME, lines)
    finally:
        conn.close()


def save_csv(file, lines):
    with open(file, 'w') as f:
        for line in lines:
            f.write(line)


if __name__ == "__main__":
    mysql_to_csv()
    csv_to_sqlite()
