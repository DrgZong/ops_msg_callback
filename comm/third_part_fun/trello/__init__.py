# !/usr/bin/env python
# @Time    : 2017/8/31 15:25
# @Author  : ZZL
# @Project : tasks_man
from trello import TrelloClient

from pw_logger import m_logger, err_logger

trello_key = "a6f690cfa23be8d366dd0dbe3d5eabd2"
trello_secret = "1954683a4ef47be218a3e78eda99d21b80d198db80f96ec6a96555f095e1e490"


def trell_client(auth):
    """
        生成trello客户端
    """
    trello_cli = None
    if auth:
        try:
            trello_cli = TrelloClient(
                api_key=trello_key,
                api_secret=trello_secret,
                token=auth.get("oauth_token", ""),
                token_secret=auth.get("oauth_token_secret", "")
            )
            m_logger.info('生成trello客户端')
        except Exception as e:
            err_logger.exception('生成github客户端失败')
    return trello_cli


def create_new_card(para, auth):
    """
    创建新的卡片
    :param para:参数字符串
    :param auth:用户授权信息
    :return:
    """
    res = None
    if para:
        trello_cli = trell_client(auth.get("trello"))
        if trello_cli:
            trello_cli.get_board()
        else:
            res = 'trello新建卡片失败，未获得授权信息'
    else:
        res = 'trello新建卡片未获得参数\n参数格式[看板名 列表名 卡片名 卡片内容]\n示例[weslack todo new_task test]'
    return res
