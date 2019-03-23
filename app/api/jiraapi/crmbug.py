"""
 封装了提 CRM bug 的接口
 Created by plough on 2018/11/20.
"""
import base64
import requests
import logging
from config import CrmConf


class CrmBugHelper:

    @classmethod
    def report_bug(cls, username, summary, desc, report_type="BUG"):
        r"""向服务器提交bug

            :param username: 提bug的用户名
            :param summary: 任务标题
            :param desc: 任务描述
            :param report_type: 类型，bug 还是需求
            :return: 服务器返回值。
                     1. 异常返回：{'errorMessages': [], 'errors': {'reporter': '指定的报告人错误。'}}
                     2. 正常返回：{'id': '201283', 'key': 'CRM-5380', 'self': 'http://www.pleasechangethis.com:6006/rest/api/2/issue/201283'}
            """
        logging.info('[report_bug] username = ' + username)
        option_map = {'reporter': {'name':username}}
        issue_id = "10104" if report_type == "BUG" else "10001"
        data = cls._create_issue("CRM", issue_id, summary, desc, option_map)
        result = cls._add_issue(data)
        logging.info('[report_bug] result = ' + str(result))
        return result

    @staticmethod
    def _create_issue(project_key, issue_id, summary, desc, option_map):
        r"""构造发送给服务器的数据内容

            :param project_key: 问题类型
            :param issue_id: bug 还是需求
            :param summary: 任务标题
            :param desc: 任务描述
            :param option_map: 其他参数
            :return: 包含数据内容的字典对象
            """

        data = {
            "fields": {
                "project": {"key": "{}".format(project_key)},
                "summary": "{}".format(summary),
                "description": "{}".format(desc),
                "issuetype": {"id": "{}".format(issue_id)}
            }
        }
        data["fields"].update(option_map)
        return data

    @classmethod
    def _add_issue(cls, data):
        r"""发送 post 请求到服务器，并返回结果

            :param data: 包含请求内容的字典
            :return: 服务器返回结果
            """
        author = "Basic " + str(base64.b64encode((CrmConf.ADMIN_NAME + ":" + CrmConf.ADMIN_PASSWORD).encode('utf-8')), 'utf-8')
        headers = {
            'Content-Type': "application/json",
            'Authorization': author
        }
        r = requests.post(CrmConf.ADD_ISSUE_URL, headers=headers, json=data)
        return r.json()


