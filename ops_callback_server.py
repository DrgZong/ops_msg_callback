#!/usr/bin/env python3
# -*-coding:utf-8-*-
"""
服务主程序
"""
import os
import sys

import tornado.httpserver
import tornado.ioloop
from tornado.options import define, options

from application import application
from pw_logger import m_logger

sys.path.append(os.path.abspath('.'))
define("port", default=8088, help="run on th given port", type=int)
define('debug', default=True, help='enable debug mode')


def main():
    """
        呵呵哒
    """
    m_logger.info('主程序启动')
    options.parse_command_line()
    # 用户行为记录线程开启
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(options.port)
    print('Development server is running at http://127.0.0.1:%s/' % options.port)
    print('Quit the server with Control-C')
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    # import pdb; pdb.set_trace()
    main()
