#!/usr/bin/env python
# ༼ꉺɷꉺ༽ coding: utf-8 ༼ꉺɷꉺ༽ 
# @Time    : 2017/8/17 16:10
# @Author  : ZZL
# @Project : tasks_man
#  ✿╹◡╹ Buddha bless me code no bug ✿╹◡╹
import datetime
import json

import requests
import hashlib

url_login = "https://www.edaice.com/mcgi/user/company_login"  # 登录
url_get_paper = "https://www.edaice.com/mcgi/topic/get_test_papers"  # 获取所有面试题
url_create_test = "https://www.edaice.com/mcgi/test/create_test"


class Edaice():
    def __init__(self, name, pwd, cookie=''):
        if cookie:
            self.cookie = cookie
        else:
            try:
                pwd = hashlib.md5(pwd.strip().encode()).hexdigest()
                res = requests.post(url_login, data={'companyId': name, "password": pwd}).json()
                if str(res.get("errcode", "-1")) == '0':
                    self.cookie = res.get("data", {}).get("sessionId")
            except Exception as e:
                self.cookie = ''
                print('Edaice init error:', str(e))

    def get_papers(self):
        res = []
        if self.cookie:
            try:
                r = requests.post(url_get_paper, data={"sessionId": self.cookie}).json()
                if str(r.get("errcode", "-1")) == '0':
                    res = r.get("data", [])
            except Exception as e:
                print('get_papers error:', str(e))
        return res

    def create_test(self, test_name, email, user_name='面试者', phone='13330211234',
                    is_moniter=1, days=7, theme='在线笔试邀请', other='请及时填写'):
        """
        发送测试邀请
        :param test_name: 测试卷题目
        :param user_name: 被邀请人名字
        :param phone: 被邀请人电话
        :param email: 被邀请人邮箱
        :param is_moniter: 是否开启监控 默认开启
        :param days: 有效期，天
        :param theme: 邮件主题
        :param other: 补充内容
        :return: 结果
        """
        res = None
        paper_id = self.get_paper_id(test_name)
        if self.cookie and test_name and email and paper_id:
            try:
                time_now = datetime.datetime.now()
                begin = str(time_now)[: str(time_now).rfind(".")]
                end = str((time_now + datetime.timedelta(days=int(days))))
                para = {"sessionId": self.cookie, "testPersonnel": user_name, "telphone": phone,
                        "email": email, "testPaperId": paper_id, "mailTheme": theme, "mailContent": other,
                        "isMonitor": is_moniter, "localTime": begin,
                        "activeTimeBegin": begin, "activeTimeEnd": end[: end.rfind(".")]}
                r = requests.post(url_create_test, data=para).json()
                if str(r.get("errcode", -1)) != '0':
                    res = json.dumps(r)
            except Exception as e:
                res = str(e)
                print('create_test error:', str(e))
        return res

    def get_paper_id(self, name):
        """
        获取试卷id
        :param name: 测试卷题目
        :return: 结果/None
        """
        res = None
        if name:
            for paper in self.get_papers():
                if name == paper.get("testPaperName", ""):
                    res = paper.get("testPaperId")
                    break
                if not res and name in paper.get("testPaperName", ""):
                    res = paper.get("testPaperId")
        return res


if __name__ == '__main__':
    ed = Edaice(None, None, "7l29k4rm8i1ezrzon07n42tl7kyx7wjcn3odk24ab6z2sd4yur")
    # print(ed.get_paper_id("题"))
    print(ed.create_test("中级前端开发工程师", "wbl", "123123123", "1803568804@qq.com"))
