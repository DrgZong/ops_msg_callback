#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
应用描述
"""
import os

import tornado.web

from url import url

setting = {
    "static_path": os.path.join(os.path.dirname(__file__), "static"),
    'xsrf_cookies': False,
}

application = tornado.web.Application(
    handlers=url,
    debug=True,
    **setting
)
