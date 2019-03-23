"""
 Created by plough on 2019/1/21.
"""
import unittest

from app.utils.wxbot_helper import WxBotHelper


class WxBotHelperTest(unittest.TestCase):

    def test_get_jira_username_by_wx_full_name(self):
        name = WxBotHelper._get_jira_username_by_wx_full_name("plough-田宗耕")
        self.assertEqual("plough", name)

        name = WxBotHelper._get_jira_username_by_wx_full_name(" jax_刘军")
        self.assertEqual("jax", name)

        name = WxBotHelper._get_jira_username_by_wx_full_name("saber-陈敏")
        self.assertEqual("chenmin", name)

        name = WxBotHelper._get_jira_username_by_wx_full_name("xuzuo.Chen(Walter)-陈栩作")
        self.assertEqual("xuzuo.chen", name)

    def test_parse_summary_and_desc_from_content(self):
        content = "CRM挂了，请尽快修复。我今天进行xx操作时发现的。"
        summary, desc = WxBotHelper.parse_summary_and_desc_from_content(content)
        self.assertEqual("CRM挂了", summary)
        self.assertEqual("请尽快修复。我今天进行xx操作时发现的。", desc)

        content = "crm挂了"
        summary, desc = WxBotHelper.parse_summary_and_desc_from_content(content)
        self.assertEqual("crm挂了", summary)
        self.assertEqual("如题", desc)

        content = "crm挂了,,,,。，，，，"
        summary, desc = WxBotHelper.parse_summary_and_desc_from_content(content)
        self.assertEqual("crm挂了", summary)
        self.assertEqual("如题", desc)

    def test_contain_keywords(self):
        content = "crm哈哈哈哈"
        self.assertTrue(WxBotHelper.contain_keywords(content))

        content = "12234566abcdef"
        self.assertFalse(WxBotHelper.contain_keywords(content))

    def test_decrypt_msg(self):
        msg_signature = '5a9d7358f419b0f5e9427f4843ad72315ad305a2'
        timestamp = '1548302915'
        nonce = '1548545132'
        encrypt_xml_data = '<xml><ToUserName><![CDATA[ww1cfe92ce0552bbe8]]></ToUserName><Encrypt><![CDATA[CmAfM8XHzDcIdqdbVbdnrhfg/88try+dspQzKMyvTQbLJAHqpdPiJThRYxBkZuVGVBcZBlJafdJYNfjxb20pSelD6ncq4sbAclOqYtv52FVm58NR05hySt+jmf2MDEUlf6I9m45xz/HdpyP4vMGRBBB3jWONn/btKrLgYYpXi3MypQhMao1ndhvFj1KdZn+Ojen+TvU6m86bnjtaQAmqVi7aCefl8FivWvMoVXQlhopsx01cXbkI1r9zqEsb5cQ2zE0YBeZp5ZmxfpOcjP78pqTt5J7hM4eadcMCh4tWxG1hwL3fu763jp7ge37QFiqLQF8Zt3s4vsEIhXbLFXi7q0FbTaitnZ00pjZ9SE5S/Ea/6PkADKWc6vpMjfm+hUOMCyEpdQPZ3o2b12JLAe6Vv5H4eddixqsYfdTLliurmwQne8OxTjBytiJJWmwDg3Tc9LIyKYSP+KjxmE7ksJPCQg==]]></Encrypt><AgentID><![CDATA[1000036]]></AgentID></xml>'
        result = WxBotHelper.decrypt_msg(msg_signature, timestamp, nonce, encrypt_xml_data)
        self.assertEqual("<xml><ToUserName><![CDATA[ww1cfe92ce0552bbe8]]></ToUserName><FromUserName><![CDATA[qy01d035f0f8b128079cdb97d5bc]]></FromUserName><CreateTime>1548302915</CreateTime><MsgType><![CDATA[event]]></MsgType><AgentID>1000036</AgentID><Event><![CDATA[enter_agent]]></Event><EventKey><![CDATA[]]></EventKey></xml>",
                         result)

if __name__ == '__main__':
    unittest.main()