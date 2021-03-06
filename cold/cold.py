#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import argparse
import os
import sqlite3
import time
import sys
from prettytable import PrettyTable

# shell params
parser = argparse.ArgumentParser("Code Start Time AVG Tool")
parser.add_argument("-p", "--package", help="application package name", required=True)
parser.add_argument("-m", "--main", help="application main activity", required=True)
parser.add_argument("-c", "--count", help="cold start time, default is 10 times", type=int, default=10)
parser.add_argument("-s", "--seconds", help="run cold start shell time interval(unit is seconds), default is 2 seconds",
                    type=int, default=2)
parser.add_argument("-v", "--verbose", help="verbosity",
                    action="store_true")
args = parser.parse_args()
package = args.package
main = args.main
count = args.count
seconds = args.seconds
verbose = args.verbose
print("package:" + package + ", main=" + main + ", count=" + str(count) + ", seconds=" + str(
    seconds) + ", verbose=" + str(verbose))

# common value
DB_NAME = "cold.db"
DROP_TABLE_TIMES = '''DROP TABLE IF EXISTS "times";'''
CREATE_TABLE_TIMES = '''
   CREATE TABLE "times" (
    "id" INTEGER PRIMARY KEY NOT NULL,
    "starting" TEXT NOT NULL,
    "status" TEXT NOT NULL,
    "activity" TEXT NOT NULL,
    "this_time" INTEGER NOT NULL,
    "total_time" INTEGER NOT NULL,
    "wait_time" INTEGER NOT NULL,
    "created_at" TEXT NOT NULL
  );
'''
INSERT_TABLE_TIMES = '''
  INSERT INTO times ("starting", "status", "activity", "this_time", "total_time", "wait_time", "created_at") 
  VALUES (?, ?, ?, ?, ?, ?, ?);
'''
QUERY_AVG_TIMES = '''
  SELECT AVG(this_time), AVG(total_time), AVG(wait_time) FROM times;
'''


def run():
    # open db
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(DROP_TABLE_TIMES)
    cursor.execute(CREATE_TABLE_TIMES)

    init()
    for i in range(1, count + 1):
        launch(cursor, i)

    rows = cursor.execute(QUERY_AVG_TIMES)
    table = PrettyTable(["Package", "Count", "Avg ThisTime", "Avg TotalTime", "Avg WaitTime", "Updated At"])
    updated_at = time.strftime("%Y-%m-%d %H:%M:%S")
    for row in rows:
        table.add_row(
            [package, count, '{:.2f}'.format(row[0]), '{:.2f}'.format(row[1]), '{:.2f}'.format(row[2]), updated_at])
        print("\033[1;32;32m" + str(table) + "\033[0m")

    # close db
    conn.commit()
    conn.close()


def init():
    # force-stop
    cmd = "adb shell am force-stop " + package
    print("[Init]>>" + cmd)
    result = os.popen(cmd)
    result.close()
    time.sleep(seconds)
    print()


# adb shell am start -W com.zui.calculator/.Calculator
# Starting: Intent { act=android.intent.action.MAIN cat=[android.intent.category.LAUNCHER]
# cmp=com.zui.calculator/.Calculator }
# Status: ok
# Activity: com.zui.calculator/.Calculator
# ThisTime: 1682
# TotalTime: 1682
# WaitTime: 1728
# Complete
#
# adb shell am force-stop com.zui.calculator
def launch(cursor, index):
    starting = ""
    status = ""
    activity = ""
    this_time = 0.0
    total_time = 0.0
    wait_time = 0.0
    created_at = time.strftime("%Y-%m-%d %H:%M:%S")
    cmd = "adb shell am start -S -W " + package + "/" + main + " -c android.intent.category.LAUNCHER -a android.intent.action.MAIN"
    print("[" + str(index) + "]>>" + cmd)
    result = os.popen(cmd)
    has_error = False
    lines = result.read().strip().split('\n')
    for line in lines:
        if "Error" in line:
            print(line)
            has_error = True
        elif "Starting" in line:
            starting = last(line)
        elif "Status" in line:
            status = last(line)
        elif "Activity" in line:
            activity = last(line)
        elif "ThisTime" in line:
            this_time = last(line)
        elif "TotalTime" in line:
            total_time = last(line)
        elif "WaitTime" in line:
            wait_time = last(line)
        else:
            continue
    result.close()
    if has_error:
        sys.exit(0)
    parameters = (starting, status, activity, this_time, total_time, wait_time, created_at)
    cursor.execute(INSERT_TABLE_TIMES, parameters)

    table = PrettyTable(["No.", "Package", "ThisTime", "TotalTime", "WaitTime", "CreatedAt"])
    table.add_row([index, package, this_time, total_time, wait_time, created_at])
    print("\033[1;33;33m" + str(table) + "\033[0m")

    cmd = "adb shell am force-stop " + package
    print("[" + str(index) + "]>>" + cmd)
    time.sleep(seconds)
    result = os.popen(cmd)
    result.close()
    print()


def last(line):
    return line.split(":")[-1].strip()


if __name__ == "__main__":
    run()
