#!/usr/bin/env python
# coding=utf-8

import sqlite3
import os

conn = sqlite3.connect(os.path.join(os.path.dirname(__file__), 'gxm.db'))
c = conn.cursor()


def init_db():
    c.execute('''CREATE TABLE stock_set(id INTEGER PRIMARY KEY AUTOINCREMENT, 
            code CHAR(10) NOT NULL, name CHAR(20) NOT NULL);''')
    c.execute('''CREATE TABLE user_stock(id INTEGER PRIMARY KEY AUTOINCREMENT, open_id CHAR(30) NOT NULL, 
            stock_code CHAR(10) NOT NULL);''')
    c.execute('''CREATE TABLE fund_set(id INTEGER PRIMARY KEY AUTOINCREMENT, 
            code CHAR(10) NOT NULL, name CHAR(20) NOT NULL);''')
    conn.commit()
    print('init database successful...')


# 批量添加股票信息
def batch_insert_stock_info(data):
    sql = "INSERT INTO stock_set (code, name) VALUES(?,?);"
    c.executemany(sql, data)
    conn.commit()


# 查询股票集合总数
def count_stock_set():
    sql = "SELECT COUNT(*) FROM stock_set;"
    c.execute(sql)
    res = c.fetchone()
    return res[0]


# 清空stock_set数据
def clear_stock_set():
    sql = "DELETE FROM stock_set;"
    c.execute(sql)
    conn.commit()


# 添加用户关注的股票code
def add_user_stock(open_id, stock_code):
    # 先校验用户是否已关注此stock_code
    sql = "SELECT * FROM user_stock WHERE open_id = '" + open_id + "' AND stock_code = '" + stock_code + "';"
    c.execute(sql)
    res = c.fetchall()
    if res.__len__() <= 0:
        sql = "INSERT INTO user_stock(open_id, stock_code) VALUES('" + open_id + "','" + stock_code + "');"
        c.execute(sql)
        conn.commit()
        return '{"code":0,"result":"成功"}'
    else:
        return '{"code":1,"result":"失败，重复添加"}'


# 根据openid查询用户关注的股票codes
def find_user_stocks(open_id):
    stocks = []
    sql = "SELECT * FROM user_stock WHERE open_id = '" + open_id + "';"
    cursor = c.execute(sql)
    for row in cursor:
        stocks.append(row[2])
    return stocks


# 根据股票名称查询code
def get_stock_code_by_name(name):
    sql = "SELECT code FROM stock_set WHERE name = '" + name + "';"
    c.execute(sql)
    res = c.fetchone()
    if res.__len__ > 0:
        return res[0]
    else:
        return None


if __name__ == "__main__":
    init_db()
    print(get_stock_code_by_name("老板电器"))
