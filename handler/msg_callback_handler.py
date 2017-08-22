#!/usr/bin/env python
# ༼ꉺɷꉺ༽ coding: utf-8 ༼ꉺɷꉺ༽ 
# @Time    : 2017/8/21 18:12
# @Author  : ZZL
# @Project : ops_msg_callback
#  ✿╹◡╹ Buddha bless me code no bug ✿╹◡╹
import json

import time
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
        self.finish(args)

    @run_on_executor
    def _post(self):
        try:
            msg = json.loads(weslack_decrypt_dict(self.request.body))
            # 模板样式待定，先实现一种:发送简历邀请及E待测试题
            """
            {'fromUserName': '@5ed299bc0c3ffc44b88bb5ebfdc0a404', 'selfRemarkName': '',
             'Username': '@@0f4cd336633e12a7e7a52064cd1ef691f44625eb4fbade89217f57b3646f8767',
              't': 1503369715, 'msgType': 'Text', 'chatroomName': 'Email透传测试群',
              'fromDisplayName': '', 'msgId': '4090747206345360890', 'atSelf': False,
              'chatroomQuanPin': 'Emailtouchuanceshiqun', 'isgroup': True, 'text': 'EE',
               'fromNickName': '宗志龙'}

            """
            print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(msg.get('t', '0'))))
                  + '   ' + msg.get("chatroomName", "xxx") + "   " + msg.get("fromNickName", "xxx") + ":"
                  + "\n" + msg.get("text", "xxx"))

        except Exception as e:
            m_logger.info('消息格式错误：%s', str(e))
        return ""

