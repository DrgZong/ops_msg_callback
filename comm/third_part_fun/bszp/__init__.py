#!/usr/bin/env python
# ༼ꉺɷꉺ༽ coding: utf-8 ༼ꉺɷꉺ༽ 
# @Time    : 2017/8/17 9:50
# @Author  : ZZL
# @Project : tasks_man
#  ✿╹◡╹ Buddha bless me code no bug ✿╹◡╹
import datetime
import json

import requests
import time

from bs4 import BeautifulSoup

from pw_logger import m_logger

url_all = "https://www.zhipin.com/chat/userList.json?page={page}&_=%s" % int(time.time())  # 全部联系人
url_new = "https://www.zhipin.com/chat/resumedirectList.json?page={page}&_=%s" % int(time.time())  # 新联系人
url_talking = "https://www.zhipin.com/chat/userfilterlist.json?page=0&status=6&origin=-1&jobid=-1&rank=1&salary=0&experience=0&degree=0&_=%s" % int(
    time.time())  # 沟通中的用户列表
url_chat_history = "https://www.zhipin.com/chat/historymsg.json?gid={gid}&maxMsgId=0&c=20&page={page}"  # 历史聊天记录
url_get_resume = "https://www.zhipin.com/chat/requestResume.json?to={gid}&_=%s" % int(time.time() * 1000)  # 邀请投递简历
url_get_user_info = "https://www.zhipin.com/chat/geek.json?uid={gid}"  # 获取某用户信息
url_send_invite = "https://www.zhipin.com/bossweb/interview/invite.json"  # 发送面试邀请
url_get_job_id = "https://www.zhipin.com/bossweb/joblist/data.json?page=1&type=0&status=1&_=%s" % int(
    time.time())  # 获取打开的职位


def get_all_user(cookie, page=1):
    """
    分页获取所有联系过的人 貌似一直为空暂时不用
    :param page: 第几页(1开始)
    :param cookie: 相当于token
    :return: 联系人列表
    """
    res = []
    try:
        resp = requests.get(url_all.format(page=page), cookies=cookie).json()
        if resp.get("status", 0) == 1:
            res = resp.get('data', [])
    except Exception as e:
        print('get_all_user error:%s', str(e))
    return res


def get_talking_user(cookie):
    """
    获取正在沟通中的人
    :param cookie: 相当于token
    :return: 联系人id列表
    """
    res = []
    try:
        resp = requests.get(url_talking, cookies=cookie).json()
        if resp.get("rescode", 0) == 1:
            res = resp.get('data', [])
    except Exception as e:
        print('get_talking_user error:%s', str(e))
    return res


def get_new_user(cookie, page=1):
    """
    分页获取新联系人
    :param cookie: 相当于token
    :param page: 第几页(1开始)
    :return: 联系人列表
    """
    res = []
    try:
        resp = requests.get(url_new.format(page=page), cookies=cookie).json()
        if resp.get("status", 0) == 1:
            res = resp.get('data', [])
    except Exception as e:
        print('get_new_user error:%s', str(e))
    return res


def get_chat_history(cookie, gid, page=1, need_detail=False):
    """
    分页获取某联系人的历史聊天记录
    :param cookie: 相当于token
    :param page: 第几页(1开始)
    :param gid: 用户id
    :param need_detail: 是否需要聊天详细信息，否则只返回联系的文本消息
    :return: 聊天记录列表
    """
    res = []
    try:
        resp = requests.get(url_chat_history.format(page=page, gid=gid), cookies=cookie).json()
        if resp.get("type", 0) == 1:
            res = resp.get('messages', [])
            if not need_detail:
                res = list(filter(None, list({'text': item.get("pushText", None),
                                              'body': item.get("body", {})} for item in res)))
    except Exception as e:
        print('get_chat_history error:%s', str(e))
    return res


def get_user_resume(cookie, gid):
    """
    获取某联系人的简历
    :param cookie: 相当于token
    :param gid: 用户id
    :return: 请求结果
    """
    res = None
    try:
        resp = requests.get(url_get_resume.format(gid=gid), cookies=cookie).json()
        if resp.get("result", 0) != 1:
            res = json.dumps(resp)
    except Exception as e:
        res = str(e)
        print('get_user_resume error:%s', str(e))
    return res


def get_user_info(cookie, gid):
    """
       获取某联系人的信息
       :param cookie: 相当于token
       :param gid: 用户id
       :return: 联系人信息
       """
    res = {}
    try:
        resp = requests.get(url_get_user_info.format(gid=gid), cookies=cookie).json()
        if resp.get("status", 0) == 1:
            res = resp.get('data', {})
    except Exception as e:
        print('get_user_info error:%s', str(e))
    return res


def send_invite(cookie, username, jobid, tips='', invite_time=''):
    """
    发送面试邀请
    :param cookie: 相当于token
    :param username: 用户名称
    :param jobid: 请求面试职位id
    :param tips: 邀请简介
    :param invite_time: 面试时间， 默认一天后的现在
    :return: 请求结果
    """
    res = None
    gid = str(get_userid(cookie, username))
    print(gid)
    if jobid and gid and gid != 'None':
        if not tips:
            tips = "给你邮箱发了一个在线笔试邀请，请于邀请时间之前做完，评卷结束后我们会通知你后续面试的时间"
        now = datetime.datetime.now()
        if invite_time:
            try:
                if len(invite_time) != 8:
                    raise Exception('time error')
                date = str(now.year) + '-' + invite_time[:2] + '-' + invite_time[2: 4]
                hour = int(invite_time[4: 6])
                minute = int(invite_time[6:])
            except Exception as e:
                res = str(e)
                return res

        else:
            date = str((now + datetime.timedelta(days=7)).date())
            hour = now.hour
            minute = now.minute
        para = {'jobid': jobid, 'date': date,
                'hour': hour, 'minute': minute, 'other': tips,
                'uid': gid, 'sendmsg': '0'}
        try:
            resp = requests.post(url_send_invite, cookies=cookie, data=para).json()
            m_logger.info("面试邀请网络返回:%s", resp)
            if resp.get("rescode", 0) != 1:
                res = resp.get('resmsg', '未知错误')
        except Exception as e:
            res = str(e)
            print('send_invite error:%s', str(e))
    else:
        res = '未找到对应用户'
    return res


def get_userid(cookie, username):
    """
       获取某联系人的id
       :param cookie: 相当于token
       :param username: 用户名称
       :return: 联系人id/None
       """
    res = None
    if username:
        page = 1
        need_break = False
        while not need_break:
            users = get_all_user(cookie, page)
            if users:
                for user in users:
                    if user.get('name', '').strip() == username.strip():
                        res = user.get('uid')
                        need_break = True
                        break
            else:
                need_break = True
            page += 1
    return res


def get_jobid(cookie, jobname):
    """
       获取某联系人的id
       :param cookie: 相当于token
       :param jobname: 职位名称
       :return: 联系人id/None
       """
    res = None
    if jobname:
        job_name = jobname.lower()
        try:
            resp = requests.get(url_get_job_id, cookies=cookie).json()
            if str(resp.get("rescode", 0)) == '1':
                html = resp.get('html', "")
                soup = BeautifulSoup(html, "html.parser")
                jobs_html = soup.find_all("tr")
                for job in jobs_html:
                    name = job.find("div", {"class": "position-title"}).find("a").string.lower()
                    if name == job_name:
                        res = job.find("a", {"class": "link-chat"}).get("data-jobid")
                        break
                    if not res and job_name in name:
                        res = job.find("a", {"class": "link-chat"}).get("data-jobid")
        except Exception as e:
            print('get_jobid error:%s', str(e))
    return res


# 以下是微信反向操作的方法，操作成功返回None否则返回错误信息
def wx_send_boss_invite(args):
    m_logger.info("发送BOSS直聘面试邀请")
    if not args:
        res = 'BOSS直聘发送面试邀请未获得参数'
    else:
        cookie = {'t': 'fPQirgQj9lzoRs', 'wt': 'fPQirgQj9lzoRs'}
        params = args.split(' ')
        if len(params) >= 2:
            job_id = get_jobid(cookie, params[0])
            if job_id:
                res = send_invite(cookie=cookie, jobid=job_id,
                                  username=params[1],
                                  invite_time=params[2] if len(params) > 2 and params[2] != '' else None,
                                  tips=params[3] if len(params) > 3 and params[3] != '' else None)
            else:
                res = "BOSS直聘发送面试邀请未查到[{}]职位".format(params[0])
        else:
            res = "BOSS直聘发送面试邀请参数不足"
    m_logger.info("发送BOSS直聘面试邀请结果：%s", res)
    return res + '\n参数格式[职位名 用户名 时间或者默认7天后的此时 提示语或者默认发送笔试邀请提示]\n' \
                 '示例[android test 08231515 诚邀面试]' if res else "BOSS直聘面试邀请发送成功"


if __name__ == '__main__':
    m_cookie = {
        't': 'fPQirgQj9lzoRs',
        'wt': 'fPQirgQj9lzoRs'
    }
    # print(send_invite(m_cookie, '王博龙', invite_time='08231717'))
    # print(get_all_user(m_cookie, 1))
    # print(get_jobid(cookie=m_cookie, jobname="ios"))
    # print(str(None))
    text = """@WeSlack客服机器人 edaice
产品 瞿秋晨 18678200082  491030748@qq.com  7"""
    text_list = text.replace('\u2005', ' ').replace('\r', ' ').split("\n")
    print(text_list)
    task_name = list(filter(None, text_list[0].split(" ")))[1].split(".")
    print(task_name)
    fun = {"edaice": {"default": "test"}}.get(task_name[0].lower(), {}). \
        get(task_name[1] if len(task_name) > 1 and task_name[1] else 'default')
    params = text_list[1].split(' ')
    print(params)