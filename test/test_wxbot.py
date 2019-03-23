"""
 Created by plough on 2018/11/20.
"""

import unittest
from unittest.mock import MagicMock

from app.api.jiraapi.crmbug import CrmBugHelper
from app.wxbot import WxBot
from config import WxBotConf, CrmConf


class WxBotTest(unittest.TestCase):

    def test_report_bug(self):
        user_id = "qy01d035f0f8b128079cdb97d5bc"

        # 若注释此行，将向真实 JIRA 服务器提交 bug
        CrmConf.ADD_ISSUE_URL = "http://httpbin.org/post"

        content_a = "hello"
        result_a = WxBot._report_bug(user_id, content_a)
        self.assertEqual("你好", result_a)

        content_b = "crm xxx"
        result_b = WxBot._report_bug(user_id, content_b)
        self.assertTrue('标题：crm' in result_b and '描述：xxx' in result_b)

        content_c = "crm,<"
        result_c = WxBot._report_bug(user_id, content_c)
        self.assertEqual(WxBotConf.INVALID_CONTENT_TIP, result_c)

        # 测试找不到用户名的情况
        CrmBugHelper.report_bug = MagicMock(return_value={'errorMessages': [], 'errors': {'reporter': '指定的报告人错误。'}})
        WxBot.report_buffer[user_id] = {'jira_username':'plough', 'summary':'test', 'desc':'test'}
        WxBot.send_bug_success_feedback = MagicMock()
        result = WxBot._report_bug(user_id, '1')
        self.assertTrue("出现异常" in result)

    def test_make_response(self):
        from_user_name = "qy01d035f0f8b128079cdb97d5bc"
        event_xml = """
            <xml><ToUserName><![CDATA[888]]></ToUserName>
            <FromUserName><![CDATA[{}]]></FromUserName>
            <CreateTime>1408091189</CreateTime>
            <MsgType><![CDATA[event]]></MsgType>
            <Event><![CDATA[enter_agent]]></Event>
            <EventKey><![CDATA[]]></EventKey>
            <AgentID>1</AgentID>
            </xml>
            """.format(from_user_name).strip()

        msg_xml = """
            <xml>
               <ToUserName><![CDATA[888]]></ToUserName>
               <FromUserName><![CDATA[{}]]></FromUserName> 
               <CreateTime>1348831860</CreateTime>
               <MsgType><![CDATA[text]]></MsgType>
               <Content><![CDATA[hello]]></Content>
               <MsgId>1234567890123456</MsgId>
               <AgentID>1</AgentID>
            </xml>
            """.format(from_user_name).strip()

        r = WxBot.make_response(event_xml)
        self.assertTrue(from_user_name in r)
        self.assertTrue(WxBotConf.FIRST_USE_TIP in r)

        # 连续触发事件时，不响应
        r = WxBot.make_response(event_xml)
        self.assertTrue(r is None)


        r = WxBot.make_response(msg_xml)
        self.assertTrue(from_user_name in r)

        r = WxBot.make_response(event_xml)
        self.assertTrue(r is None)


if __name__ == '__main__':
    unittest.main()