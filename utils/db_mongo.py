#!/usr/bin/env python
# coding=utf-8

from pymongo import MongoClient

client = MongoClient()
db = client.gxm
stock_set = db.stock_set


def find_stocks_by_user(user_openid):
    result = stock_set.find_one({"_id": user_openid})
    return result


if __name__ == "__main__":
    # stock_set.insert({"_id": "001", "name": "zhangsan", "age": 18})
    print(find_stocks_by_user("001"))
