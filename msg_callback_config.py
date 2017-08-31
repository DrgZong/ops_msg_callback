from comm.third_part_fun.bszp import wx_send_boss_invite
from comm.third_part_fun.edaice import wx_send_test
from comm.third_part_fun.trello import create_new_card

task = {
    "boss": {
        "invite": wx_send_boss_invite,  # 发送boss面试邀请，格式为【职位 用户名 时间(08231515)或者不写 提示语或者不写】
        "default": wx_send_boss_invite,
    },
    "edaice": {
        "test": wx_send_test,
        "default": wx_send_test,  # 发送e待测笔试 格式为【试卷名(模糊) 用户 电话 邮箱 有效期或者不写】
    },
    "trello": {
        "default": create_new_card,  # 创建trello新卡片 格式为【试卷名(模糊)|邮箱|有效期或者不屑】
    }
}

if __name__ == '__main__':
    print(task.get("boss").get("invite"))
