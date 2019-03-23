"""
 图灵机器人 api 测试
 Created by plough on 2018/11/21.
"""

import unittest

from app.api.turingapi.turingbot import TuringBot


class TuringBotTest(unittest.TestCase):

    def test_ask_turing_bot(self):
        result = TuringBot.ask_turing_bot('hello')
        self.assertEqual('你好', result)

        # 可以查询天气
        result = TuringBot.ask_turing_bot('南京的天气')
        self.assertTrue(result.startswith('南京:'))



if __name__ == '__main__':
    unittest.main()