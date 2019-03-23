"""
 Created by plough on 2019/1/21.
"""

import unittest

from app.utils.wx_manager import WxManager


class WxManagerTest(unittest.TestCase):

    def setUp(self):
        self.test_chat_id = '11933413116216068339'  # 微信提bug机器人设计、开发、测试讨论
        self.user_id = 'qy01d035f0f8b128079cdb97d5bc'  # plough

    def test_create_group(self):
        name = 'WxBot帆软全员通知群'
        owner_id = 'qy01d035f0f8b128079cdb97d5bc'
        user_list = [owner_id, 'Manto']
        chat_id = 'wxbot0crmbug0group'
        # 打开此注释，可以用机器人创建新的讨论群组（先修改chat_id）
        # WxManager.create_group(name, owner_id, user_list, chat_id)

    def test_send_msg_to_group(self):
        WxManager.send_text_msg_to_group(self.test_chat_id, "大家好，机器人正式上线了，如果要给 crm 提 bug，请私聊我～")

    def test_send_card_msg_to_group(self):
        # content = '吧啦吧啦吧啦吧啦吧啦吧啦吧啦吧啦吧啦吧啦吧啦吧啦' * 10
        content =  '吧dsfds f啦吧aadjfdnsv slnf啦sdf啦j,,,sjdfljds啦'*10

        bug_info = {
            "jira_username": 'Plough',
            "summary": 'crm又挂了',
            "desc": content
        }
        WxManager.send_card_msg_to_group(self.test_chat_id, 'CRM-2334', bug_info)

    def test_send_text_msg_to_wx_user(self):
        WxManager.send_text_msg_to_wx_user(self.user_id, "你好～")

    def test_get_wx_username_by_wx_userid(self):
        wx_username = WxManager.get_wx_username_by_wx_userid(self.user_id)
        self.assertEqual("plough-田宗耕", wx_username)


if __name__ == '__main__':
    unittest.main()