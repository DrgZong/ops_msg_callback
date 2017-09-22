#!/usr/bin/env python
# ༼ꉺɷꉺ༽ coding: utf-8 ༼ꉺɷꉺ༽ 
# @Time    : 2017/8/21 18:22
# @Author  : ZZL
# @Project : ops_msg_callback
#  ✿╹◡╹ Buddha bless me code no bug ✿╹◡╹
import json

import requests
import time
from cryptography.fernet import Fernet

from weslack_config import secret, task_man_url, login_url

cookie_dic = {}


def weslack_decrypt_dict(encrypt_str):
    """
        解密数据
    """
    if isinstance(encrypt_str, str):
        msg_bytes = encrypt_str.encode()  # 编码为bytes
    else:
        msg_bytes = encrypt_str
    f = Fernet(secret.encode())
    return f.decrypt(msg_bytes).decode()  # 解码并转换为字符串


def weslack_encrypt_dict(d):
    """
        加密字典格式
    """
    if isinstance(d, dict):
        msg_str = json.dumps(d).encode()  # json转化字典为字符串,并编码为bytes
    elif isinstance(d, str):
        msg_str = d.encode()
    elif isinstance(d, bytes):
        msg_str = d
    else:
        msg_str = str(d).encode()
    f = Fernet(secret)
    return f.encrypt(msg_str).decode()  # 经过加密并转换为字符串


def get_cookie():
    global cookie_dic
    if cookie_dic and cookie_dic.get("expired") >= int(time.time()):
        res = cookie_dic.get("cookie")
    else:
        res = requests.post(login_url).cookies.get("weslackuser")
        cookie_dic = {
            "cookie": res,
            "expired": int(time.time() + 9 * 24 * 3600)
        }
    return res


def send_wx_msg(text, to, is_group=True):
    res = None
    if text and to:
        data = {"text": text, "username": to, "isgroup": is_group}
        res = requests.post(task_man_url, cookies={"weslackuser": get_cookie()}, data={
            "descpt": weslack_encrypt_dict(data),
        }).text
    return res
