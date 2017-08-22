#!/usr/bin/env python
# ༼ꉺɷꉺ༽ coding: utf-8 ༼ꉺɷꉺ༽ 
# @Time    : 2017/8/21 18:12
# @Author  : ZZL
# @Project : ops_msg_callback
#  ✿╹◡╹ Buddha bless me code no bug ✿╹◡╹
import json

import tornado.web
import tornado.gen
from tornado.concurrent import run_on_executor

from comm.weslack_fun import weslack_decrypt_dict
from handler.base import BaseHandler
from pw_logger import m_logger


class MsgCallback(BaseHandler):
    def get(self):
        self.finish('ok')

    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def post(self):
        args = yield self._post()
        print(args)
        self.finish(json.dumps(args))

    @run_on_executor
    def _post(self):
        try:
            msg = json.loads(weslack_decrypt_dict(self.request.body.decode("utf-8")))
            # 模板样式待定，先实现一种:发送简历邀请及E待测试题
            print(msg)

        except Exception as e:
            m_logger.info('消息格式错误：%s', str(e))
        return {"msg": ""}

