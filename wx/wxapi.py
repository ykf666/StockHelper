#!/usr/bin/env python
# coding=utf-8
import random
import string
import hashlib
from requests import get
import json
from WXMsgCrypt import WXBizMsgCrypt

account = "gh_fd46ac560288"
wx_token = "RZmUQDAuNjf3y6i2kL0IX8WBMOpPraEY"
wx_encodingAESKey = "z4dGm7I9k5xtPDj7ucLgHK0xwCoIVGFOuOW90cOsnga"
wx_appid = "wx22b402d2c52b8ac1"


def get_access_token():
    resp = get("https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&"
               "appid=wx22b402d2c52b8ac1&secret=35f4c38e139897fd17a668eb3144de44")
    resp = json.loads(resp.json())
    return resp["access_token"]


def decrypt(from_xml, msg_sign, timestamp, nonce):
    process = WXBizMsgCrypt(wx_token, wx_encodingAESKey, wx_appid)
    ret, decryp_xml = process.DecryptMsg(from_xml, msg_sign, timestamp, nonce)
    return ret, decryp_xml


# 生成token时使用
def gen_random_str(length):
    ran_str = ''.join(random.sample(string.ascii_letters + string.digits, length))
    print(ran_str)


# 微信公众号配置服务器时，校验加密字符串
def check_signature():
    params = {'signature': 'b52ea599227c8caef923088e092ef0ac6a6435c1',
              'echostr': '2332794040598056927',
              'timestamp': '1514441631',
              'nonce': '4233655036'
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


if __name__ == "__main__":
    print(check_signature())
