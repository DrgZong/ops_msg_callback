#!/usr/bin/env python3
# coding:utf-8
"""
url路由管理
"""
from handler.msg_callback_handler import MsgCallback

url = [
    (r"/wxmsg_callback", MsgCallback),  # ops发送微信消息回调
]
