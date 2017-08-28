#!/usr/bin/env python3
# coding:utf-8
'''
    handler父类
'''
from concurrent.futures import ThreadPoolExecutor
import tornado.web


class BaseHandler(tornado.web.RequestHandler):
    """
        自定义handler父类
    """
    # 线程执行器,供子类继承使用
    executor = ThreadPoolExecutor()

    def data_received(self, chunk):
        pass

    def on_finish(self):
        self.total_time = self.request._finish_time - self.request._start_time

    def v_finish(self, *arg, **argv):
        print(self.self.total_time)
        if arg:
            self.finish(arg[0])
        else:
            self.finish("")