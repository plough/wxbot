"""
 图灵机器人接口
 Created by plough on 2018/11/21.
"""
import json

import requests

from config import TuringConf


class TuringBot:

    # TODO：这里用 json.dump 应该更好些
    template = '''
        {
            "reqType":0,
            "perception": {
                "inputText": {
                    "text": "%s"
                }
            },
            "userInfo": {
                "apiKey": "%s",
                "userId": "%s"
            }
        }'''

    @classmethod
    def ask_turing_bot(cls, text):
        data = json.loads(cls.template % (text, TuringConf.API_KEY, TuringConf.USER_ID))
        headers = {
            'Content-Type': "application/json"
        }
        r = requests.post(TuringConf.URL, headers=headers, json=data).json()

        if 'results' not in r:
            return text

        results = r['results']
        for result in results:
            if result['resultType'] == 'text':
                return result['values']['text']
        return text