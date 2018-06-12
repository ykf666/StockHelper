#!/usr/bin/env python
# coding=utf-8

import sqlite3

conn = sqlite3.connect('gxm.db')
c = conn.cursor()


def init_db():
    c.execute('''CREATE TABLE stock_set(code CHAR(10) PRIMARY KEY, name CHAR(20) NOT NULL);''')
    c.execute('''CREATE TABLE fund_set(code CHAR(10) PRIMARY KEY, name CHAR(20) NOT NULL);''')
    c.execute('''CREATE TABLE user_stock(id INTEGER PRIMARY KEY AUTOINCREMENT, open_id CHAR(30) NOT NULL, 
            stock_code CHAR(10) NOT NULL);''')
    conn.commit()
    print('init database successful...')


# 添加股票信息
def add_stock_info(stock_code, stock_name):
    sql = "INSERT INTO stock_set(code, name) VALUES('" + stock_code + "','" + stock_name + "');"
    c.execute(sql)
    conn.commit()


# 添加用户关注的股票code
def add_user_stock(open_id, stock_code):
    # 先校验用户是否已关注此stock_code
    sql = "SELECT * FROM user_stock WHERE open_id = '" + open_id + "' AND stock_code = '" + stock_code + "';"
    cursor = c.execute(sql)
    for row in cursor:
        print(row[2])
    #     sql = "INSERT INTO user_stock(open_id, stock_code) VALUES('" + open_id + "','" + stock_code + "');"
    #     c.execute(sql)
    #     conn.commit()


# 根据openid查询用户关注的股票codes
def find_stocks_user(open_id):
    list = []
    sql = "SELECT * FROM user_stock WHERE open_id = '" + open_id + "';"
    cursor = c.execute(sql)
    for row in cursor:
        list.append(row[2])
    return ",".join(list)


if __name__ == "__main__":
    add_user_stock("sdfsdfs", "123321")
    print(find_stocks_user("sdfsdfs"))