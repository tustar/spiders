#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import logging
import sqlite3

logging.basicConfig(level=logging.DEBUG,
                    format='%(levelname)s %(asctime)s %(filename)s %(funcName)s [line:%(lineno)d] %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')

DB_NAME = "food.db"
SELECT_SQL = "SELECT * FROM food WHERE name LIKE '%又叫%'"


def analysis_food_db():
    # open db
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(SELECT_SQL)
    rows = cursor.fetchall()
    sqls = []
    comment = "Update %d cn(hk) name" % len(rows)
    logging.debug(comment)
    sqls.append("-- %s" % comment)
    for row in rows:
        id = row[0]
        # category_id = row[1]
        # calory = row[2]
        # weight = row[3]
        # code = row[4]
        name = row[5]
        # name_en = row[6]
        name_hk = row[7]
        new_name = update_name(id, name)
        new_name_hk = update_name(id, name_hk)
        sqls.append("-- id:%d cn: [%s => %s], hk: [%s => %s]" % (id, name, new_name, name_hk, new_name_hk))
        update_sql = "UPDATE food SET name='%s', name_hk='%s' WHERE id=%d;" % (update_sql_name(new_name), update_sql_name(new_name_hk), id)
        sqls.append(update_sql)
        cursor.execute(update_sql)

    write_update_sql(sqls)

    # close db
    conn.commit()
    conn.close()


def update_name(id, name):
    new_name = name.replace("，又叫...", "") \
        .replace("又叫", "") \
        .replace("...", "") \
        .replace("、", "，")
    logging.debug("%d:[%s => %s]" % (id, name, new_name))
    return new_name


def update_sql_name(name):
    new_name = name.replace("'", "''")
    return new_name


def write_update_sql(sqls):
    filename = 'food_db_migration_1_2.sql'
    with open(filename, 'w') as f:
        for sql in sqls:
            f.write("%s\n" % sql)


if __name__ == "__main__":
    analysis_food_db()
