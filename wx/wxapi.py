#!/usr/bin/env python
# coding=utf-8
import random
import string
import hashlib
from requests import get
from libs.WXMsgCrypt import WXBizMsgCrypt
import xml.etree.cElementTree as ET
import json

wx_account = "gh_fd46ac560288"
wx_token = "RZmUQDAuNjf3y6i2kL0IX8WBMOpPraEY"
wx_encodingAESKey = "z4dGm7I9k5xtPDj7ucLgHK0xwCoIVGFOuOW90cOsnga"
wx_appid = "wx22b402d2c52b8ac1"
process = WXBizMsgCrypt.WXBizMsgCrypt(wx_token, wx_encodingAESKey, wx_appid)


def get_access_token():
    resp = get("https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&"
               "appid=wx22b402d2c52b8ac1&secret=0c04e10dad27f8b8803d3230c72ec7e3")
    t = resp.text
    d = json.loads(t)
    return d['access_token']


def decrypt(from_xml, msg_sign, timestamp, nonce):
    ret, decryp_xml = process.DecryptMsg(from_xml, msg_sign, timestamp, nonce)
    return ret, decryp_xml


def encrypt(to_xml, nonce):
    ret, encrypt_xml = process.EncryptMsg(to_xml, nonce)
    return ret, encrypt_xml


def get_random_int():
    return random.randint(0, 2 ** 64 - 1)


# 解析xml，获取nodename节点的值
def extract(xmltext, nodename):
    try:
        xml_tree = ET.fromstring(xmltext)
        node = xml_tree.find(nodename)
        return node.text
    except Exception as e:
        print(e)
        return None


# 1、微信后台设置token令牌时使用，32位字符串
# 2、返回消息时，生成随机字符串，8位字符串
def get_random_str(strlen):
    ran_str = ''.join(random.sample(string.ascii_letters + string.digits, strlen))
    return ran_str


# 微信公众号配置服务器时，校验加密字符串
def check_signature(signature, timestamp, nonce):
    params = {'signature': signature,
              'timestamp': timestamp,
              'nonce': nonce
              }
    # 排序
    list_param = [wx_token, params["timestamp"], params["nonce"]]
    list_param.sort()
    # 字符串拼接
    t = list_param[0] + list_param[1] + list_param[2]
    print(t)
    encrystr = hashlib.sha1(t.encode("utf-8")).hexdigest()
    print(encrystr)
    return params["signature"] == encrystr
