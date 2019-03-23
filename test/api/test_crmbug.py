"""
 Created by plough on 2018/11/20.
"""
import unittest

from app.api.jiraapi.crmbug import CrmBugHelper
from config import CrmConf


class CrmBugHelperTest(unittest.TestCase):

    def test_report_bug(self):
        # 使用 mock 服务器跑单元测试。注释此行，则使用真实 JIRA 服务器
        CrmConf.ADD_ISSUE_URL = "http://httpbin.org/post"

        result = CrmBugHelper.report_bug("plough", "测试", "这是一条测试消息，请忽略", "BUG")
        print(result)
        self.assertEqual(5, len(result['json']['fields']))



if __name__ == '__main__':
    unittest.main()