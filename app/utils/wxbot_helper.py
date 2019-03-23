"""
 Created by plough on 2019/1/21.
"""
import re
import sys

from app.utils.callback.WXBizMsgCrypt import WXBizMsgCrypt
from app.utils.wx_manager import WxManager
from config import WxConf, WxBotConf


class WxBotHelper:
    wx_crypt = WXBizMsgCrypt(WxConf.APP_TOKEN, WxConf.APP_ENCODING_AES_KEY, WxConf.CORP_ID)
    chat_id = WxBotConf.CHAT_ID

    @classmethod
    def verify_url(cls, args):
        r"""封装 token 验证逻辑"""

        ret, reply_echo_str = cls.wx_crypt.VerifyURL(
            args['msg_signature'],
            args['timestamp'],
            args['nonce'],
            args['echostr']
        )

        if ret != 0:
            print("ERR: VerifyURL ret: " + str(ret))
            sys.exit(1)

        return reply_echo_str

    @classmethod
    def decrypt_msg(cls, s_msg_signature, s_timestamp, s_nonce, encrypt_xml_data):
        r""" 解密消息

        :param s_msg_signature: 消息签名
        :param s_timestamp: 时间戳
        :param s_nonce: 随机数
        :param encrypt_xml_data: 已加密的xml
        :return: xml 格式的明文
        """
        ret, s_xml_content = cls.wx_crypt.DecryptMsg(encrypt_xml_data, s_msg_signature, s_timestamp, s_nonce)
        print(ret, s_xml_content)
        if ret != 0:
            print("ERR: DecryptMsg ret: " + str(ret))
            sys.exit(1)
            # 解密成功，s_xml_content 即为 xml 格式的明文
        return s_xml_content

    @classmethod
    def encrypt_msg(cls, s_msg_xml, s_nonce, s_timestamp):
        r""" 加密消息

        :param s_msg_xml: xml消息明文
        :param s_nonce: 随机数
        :param s_timestamp: 时间戳
        :return: xml加密后的结果
        """
        ret, s_encrypt_msg = cls.wx_crypt.EncryptMsg(s_msg_xml, s_nonce, s_timestamp)
        if ret != 0:
            print("ERR: EncryptMsg ret: " + str(ret))
            sys.exit(1)
        # ret == 0 加密成功，企业需要将sEncryptMsg返回给企业号
        return s_encrypt_msg

    @staticmethod
    def get_jira_username_by_wx_userid(user_id):
        r""" 从微信的用户id（不是用户名），解析出对应的JIRA用户名

        :param user_id: 微信用户id
        :return: JIRA 用户名
        """
        wx_full_name = WxManager.get_wx_username_by_wx_userid(user_id)
        jira_name = WxBotHelper._get_jira_username_by_wx_full_name(wx_full_name)
        return jira_name

    @staticmethod
    def _get_jira_username_by_wx_full_name(wx_full_name):
        wx_short_name = WxBotHelper._get_wx_short_name_by_wx_full_name(wx_full_name)
        jira_name = WxBotHelper._translate_wx_short_name_to_jira_name(wx_short_name)
        return jira_name

    @classmethod
    def send_bug_success_feedback(cls, bug_num, user_id, bug_info):
        """发送已提交的bug链接给相关用户和 crm 群"""

        content = WxBotConf.BUG_REPORT_INFO_USER.format(bug_num)

        WxManager.send_text_msg_to_wx_user(user_id, content)
        WxManager.send_card_msg_to_group(cls.chat_id, bug_num, bug_info)

    @staticmethod
    def _get_wx_short_name_by_wx_full_name(wx_full_name):
        wx_name = re.split(r'[-|_]', wx_full_name)[0]
        return wx_name.strip()

    @staticmethod
    def _translate_wx_short_name_to_jira_name(wx_short_name):
        """有的人微信名跟JIRA名不一样，需要加一层映射过滤"""
        wx_jira_name_map = WxBotConf.WX_JIRA_NAME_MAP
        if wx_short_name in wx_jira_name_map:
            return wx_jira_name_map[wx_short_name]
        return wx_short_name

    @staticmethod
    def get_res_xml(from_user_id, res_content):
        r""" 构造返回给微信服务器的 xml

        :param from_user_id: 发送原始消息的微信用户id
        :param res_content: 响应给用户的纯文本内容
        :return: 包装好，待返回的 xml 明文
        """
        res_xml_template = "<xml><ToUserName>{}</ToUserName><FromUserName>{}</FromUserName><CreateTime>1476422779</CreateTime><MsgType>text</MsgType><Content>{}</Content><MsgId>1456453720</MsgId><AgentID>{}</AgentID></xml>"
        return res_xml_template.format(WxConf.CORP_ID, from_user_id, res_content, WxConf.APP_ID)

    @staticmethod
    def parse_summary_and_desc_from_content(content):
        r""" 从用户输入的字符串中，解析出 BUG 标题和详情

        :param content: 包含bug关键字的纯文本
        :return: (标题，详情)
        """

        # 用第一个标点符号作分隔符。标点之前的内容为标题，标点之后的内容为详情。
        summary = re.split(r'[^\w]', content)[0]
        desc = content.replace(summary, '', 1)
        words = re.findall('\w', desc)
        # 如果没有标点，或者标点之后没有内容，则详情内容为"如题"
        if len(words) == 0:
            desc = '如题'
        else:
            first_word = words[0]
            start_index = desc.find(first_word)
            desc = desc[start_index:]
        return summary, desc

    @classmethod
    def contain_keywords(cls, content):
        r""" 检测字符串中是否包含提bug关键词

        :param content: 待检测字符串
        :return: Boolean 是否包含关键词
        """
        key_words = WxBotConf.BUG_KEY_WORDS
        has_key = False
        for key_word in key_words:
            if key_word in content:
                has_key = True
                break
        return has_key
