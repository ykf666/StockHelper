#!/usr/bin/env python
# coding=utf-8

from pymongo import MongoClient

client = MongoClient("127.0.0.1", 27117)
db = client.gxm
stock_set = db.stock_set
user_stock_set = db.user_stock


# 根据openid查询用户关注的股票信息
def find_stocks_user(user_openid):
    result = user_stock_set.find_one({"openid": user_openid})
    return result


# 更新用户关注的股票信息
def update_stocks_user(user_openid, stock_code):
    result = user_stock_set.find_one({"openid": user_openid})
    if result is None:
        user_stock_set.insert_one({"openid": user_openid, "stock_codes": stock_code})
    else:
        old_stocks = result["stock_codes"]
        iscontain = old_stocks.find(stock_code)
        if iscontain == -1:
            new_stocks = old_stocks + "," + stock_code
            result["stock_codes"] = new_stocks
            user_stock_set.update({"openid": user_openid}, {"$set": result})


# 查询股票集合总数
def stock_set_count():
    return stock_set.count()


# 添加股票信息
def add_stock_info(stock_code, stock_name):
    stock_set.insert_one({"code": stock_code, "name": stock_name})


# 更新股票名称
def update_stock_info(stock_code, new_name):
    result = stock_set.find_one({"code": stock_code})
    if result is None:
        add_stock_info(stock_code, new_name)
    else:
        old_name = result["name"]
        if new_name != old_name:
            result["name"] = new_name
            stock_set.update({"code": stock_code}, {"$set": result})


# 根据股票名称查询code
def get_stock_code_by_name(name):
    result = stock_set.find_one({"name": name})
    if result is not None:
        return result["code"]
    return None


if __name__ == "__main__":
    update_stocks_user("001", "2234")
    print(find_stocks_user("001"))