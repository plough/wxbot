"""
 管理与企业微信直接交互的一些方法
 Created by plough on 2019/1/21.
"""
from app.api.wxapi.CorpApi import CorpApi, CORP_API_TYPE
from config import WxConf, WxBotConf


class WxManager:

    api = CorpApi(WxConf.CORP_ID, WxConf.APP_SECRET)

    @classmethod
    def create_group(cls, name, owner_id, user_list, new_chat_id):
        r"""新建讨论组

        :param name: 讨论组名字
        :param owner_id: 群主id
        :param user_list: 成员列表
        :param new_chat_id: 将要创建的讨论组的id
        """
        response = cls.api.httpCall(
            CORP_API_TYPE['APP_CHAT_CREATE'],
            {
                'name': name,
                'owner': owner_id,
                'userlist': user_list,
                'chatid': new_chat_id,
            })
        print(response)

    @classmethod
    def send_text_msg_to_group(cls, chat_id, content='我是文本消息热爱祖国热爱人民热爱中国共产党b'):
        r"""向指定讨论组发送文字消息

        :param chat_id: 讨论组id
        :param content: 文字消息内容
        """
        response = cls.api.httpCall(
            CORP_API_TYPE['APP_CHAT_SEND'],
            {
                'chatid': chat_id,
                'msgtype': 'text',
                'text': {
                    'content': content
                },
                'safe': 0,
            })
        print(response)

    @classmethod
    def send_card_msg_to_group(cls, chat_id, bug_num, bug_info):
        r"""向指定讨论组发送卡片消息（支持跳转 url）

        :param chat_id: 讨论组id
        :param bug_num: JIRA bug 编号
        :param bug_info: bug 的详细信息
        """

        bug_desc = bug_info['desc']
        if len(bug_desc) > WxBotConf.MAX_GROUP_DESC_WORD_NUMBER:
            bug_desc = bug_desc[:WxBotConf.MAX_GROUP_DESC_WORD_NUMBER] + "..."
        msg_content = WxBotConf.BUG_REPORT_INFO_GROUP.format(bug_info['jira_username'], bug_num, bug_info['summary'],
                                                         bug_desc)

        response = cls.api.httpCall(
            CORP_API_TYPE['APP_CHAT_SEND'],
            {
                "chatid": chat_id,
                "msgtype": "textcard",
                "textcard": {
                    "title": WxBotConf.CARD_MSG_TITLE,
                    "description": "<div class=\"normal\">{}</div>".format(msg_content),
                    "url": WxBotConf.BUG_URL_TEMPLATE.format(bug_num),
                    "btntxt": "详情"
                },
                "safe": 0
            }
        )
        print(response)

    @classmethod
    def send_text_msg_to_wx_user(cls, user_id, content):
        r""" 向微信用户发送文字消息

        :param user_id: 微信用户id
        :param content: 文本消息内容
        """
        response = cls.api.httpCall(
            CORP_API_TYPE['MESSAGE_SEND'],
            {
                "touser": user_id,
                "msgtype": "text",
                "agentid": WxConf.APP_ID,
                "text": {
                    "content": content
                },
                "safe": 0
            })
        print(response)

    @classmethod
    def get_wx_username_by_wx_userid(cls, user_id):
        r""" 获取"用户ID"对应的"用户名"

        :param user_id: 用户ID
        :return: 微信用户名
        """
        response = cls.api.httpCall(
            CORP_API_TYPE['USER_GET'],
            {
                'userid': user_id
            })
        return response['name']