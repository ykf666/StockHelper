#!/usr/bin/env python
# coding=utf-8

from pymongo import MongoClient

client = MongoClient("127.0.0.1", 27117)
db = client.gxm
stock_set = db.stock_set


def find_stocks_by_user(user_openid):
    result = stock_set.find_one({"_id": user_openid})
    return result


def stock_set_count():
    return stock_set.count()


def add_stock_info(stock_code, stock_name):
    stock_set.insert_one({"code": stock_code, "name": stock_name})


def update_stock_info(stock_code, new_name):
    result = stock_set.find_one({"code": stock_code})
    if result is None:
        add_stock_info(stock_code, new_name)
    else:
        old_name = result["name"]
        if new_name != old_name:
            result["name"] = new_name
            stock_set.update({"code": stock_code}, {"$set": result})


if __name__ == "__main__":
    # stock_set.insert({"_id": "001", "name": "zhangsan", "age": 18})
    print(find_stocks_by_user("001"))
