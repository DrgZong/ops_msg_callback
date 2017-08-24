#!/usr/bin/env python
# ༼ꉺɷꉺ༽ coding: utf-8 ༼ꉺɷꉺ༽ 
# @Time    : 2017/8/21 18:12
# @Author  : ZZL
# @Project : ops_msg_callback
#  ✿╹◡╹ Buddha bless me code no bug ✿╹◡╹
import json

import tornado.gen
import tornado.web
from tornado.concurrent import run_on_executor

from comm.weslack_fun import weslack_decrypt_dict
from handler.base import BaseHandler
from msg_callback_config import task
from pw_logger import m_logger


class MsgCallback(BaseHandler):
    def get(self):
        self.finish('ok')

    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def post(self):
        args = yield self._post()
        self.finish(args)

    @run_on_executor
    def _post(self):
        res = None
        try:
            msg = json.loads(weslack_decrypt_dict(self.request.body))
            text = msg.get("text", "xxx")
            # 模板样式待定，先实现一种:发送简历邀请及E待测试题
            if msg.get("atSelf", False) and isinstance(text, str) and "@all" not in text.lower():
                m_logger.info("手动操作消息：%s", text)
                text_list = text.replace('\u2005', ' ').split("\n")
                task_name = list(filter(None, text_list[0].split(" ")))[1].split(".")
                fun = task.get(task_name[0].lower(), {}).\
                    get(task_name[1] if len(task_name) > 1 and task_name[1] else 'default')
                if fun:
                    res = fun(text_list[1] if len(text_list) > 1 else None)
                # else:
                #     res = 'I do not support this operate'
            else:
                print(text)
        except Exception as e:
            m_logger.info('消息格式错误：%s', str(e))
        return "" if not res else res
