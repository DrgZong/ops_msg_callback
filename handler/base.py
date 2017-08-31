#!/usr/bin/env python3
# coding:utf-8
'''
    handler父类
'''
import json
from concurrent.futures import ThreadPoolExecutor

import time
import tornado.web

from comm.db_fun import get_user_auth
from comm.weslack_fun import weslack_decrypt_dict, send_wx_msg
from pw_logger import m_logger


class BaseHandler(tornado.web.RequestHandler):
    """
        自定义handler父类
    """
    # 线程执行器,供子类继承使用
    executor = ThreadPoolExecutor()

    def data_received(self, chunk):
        pass

    def post(self):
        try:
            self.msg = json.loads(weslack_decrypt_dict(self.request.body))
            self.auth = get_user_auth(self.msg.get("chatroomName", ""))
            self.do_post()
        except Exception as e:
            m_logger.info('消息格式错误：%s', str(e))
            self.v_finish("")

    def do_post(self):
        pass

    def v_finish(self, ret):
        if ret:
            if time.time() - self.request._start_time > 2:
                if self.msg:
                    send_wx_msg(ret, self.msg.get("Username", self.msg.get("isgroup")))
            else:
                self.finish(ret)
        else:
            self.finish("")
