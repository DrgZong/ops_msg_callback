#!/usr/bin/env python
# ༼ꉺɷꉺ༽ coding: utf-8 ༼ꉺɷꉺ༽ 
# @Time    : 2017/8/21 18:22
# @Author  : ZZL
# @Project : ops_msg_callback
#  ✿╹◡╹ Buddha bless me code no bug ✿╹◡╹
from cryptography.fernet import Fernet


# 30rWQkOzH0JBEOenusV31pGtKhhBcn2mMZB165bpkYI=  onlinetest 的密匙

def weslack_decrypt_dict(encrypt_str, secret='30rWQkOzH0JBEOenusV31pGtKhhBcn2mMZB165bpkYI='):
    """
        解密数据
    """
    if isinstance(secret, str):
        secret = secret.encode()
    if isinstance(encrypt_str, str):
        msg_bytes = encrypt_str.encode()  # 编码为bytes
    else:
        msg_bytes = encrypt_str
    f = Fernet(secret)
    return f.decrypt(msg_bytes).decode()  # 解码并转换为字符串
