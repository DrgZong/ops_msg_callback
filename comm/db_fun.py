# !/usr/bin/env python
# @Time    : 2017/8/31 15:25
# @Author  : ZZL
# @Project : tasks_man
from tornado.options import options


def get_user_auth(wxgroup):
    """
    通过微信群获取用户授权信息
    :param wxgroup: 微信群
    :return:认证信息
    """
    res = {}
    if wxgroup:
        res = options.mdb['user'].find_one({"wx_groups": wxgroup}, {'_id': 0, 'oauth_cred': 1})
        if res:
            res = res.get('oauth_cred', {})
    return res


if __name__ == '__main__':
    pass
