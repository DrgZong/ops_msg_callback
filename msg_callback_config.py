from comm.third_part_fun.bszp import wx_send_boss_invite
from comm.third_part_fun.edaice import wx_send_test

task = {
    "boss": {
        "invite": wx_send_boss_invite,  # 格式为【用户名|时间(08231515)或者不写|提示语或者不写】
        "default": wx_send_boss_invite,
    },
    "edaice": {
        "test": wx_send_test,
        "default": wx_send_test,  # 格式为【试卷名(模糊)|邮箱|有效期或者不屑】
    }
}

if __name__ == '__main__':
    print(task.get("boss").get("invite"))
