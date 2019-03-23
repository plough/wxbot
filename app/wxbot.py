#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
 核心业务对象
 Created by plough on 2018/11/16.
"""
import datetime
import logging
import re
from xml.etree import ElementTree as ET

from app.api.jiraapi.crmbug import CrmBugHelper
from app.api.turingapi.turingbot import TuringBot
from app.utils.wxbot_helper import WxBotHelper
from config import WxBotConf


class WxBot:
    # TODO: 全是静态方法或类方法，有可能存在并发问题

    # 缓存企业微信用户的待提交的bug信息，等确认后，再提交到 JIRA
    report_buffer = {}
    # 存储微信用户id和日期组合而成的元组，形如 {('Manto', '2018-11-22')}
    just_showed_tip_buffer = set()

    @classmethod
    def make_response(cls, s_xml_content):
        r"""解析请求xml，处理之后，返回响应xml

            :param s_xml_content: 请求携带的 xml 明文
            :return: 响应的 xml 明文
            """
        root = ET.XML(s_xml_content)
        from_user_id = root.find('FromUserName').text
        msg_type = root.find('MsgType').text

        s_today = str(datetime.date.today())
        from_user_with_date = (from_user_id, s_today)

        if msg_type == 'event' and root.find('Event').text == 'enter_agent':  # 用户进入应用的事件
            # 每天最多只对同一用户显示一次初次使用提示
            cls._clear_outdated_showed_tip_buffer(s_today)
            if from_user_with_date in cls.just_showed_tip_buffer:
                return None
            res_content = WxBotConf.FIRST_USE_TIP
            cls.just_showed_tip_buffer.add(from_user_with_date)
        elif msg_type == 'text':
            # 用户输入文字，走正常的响应流程
            content = root.find('Content').text
            res_content = WxBot._report_bug(from_user_id, content)
        else:  # 其他情况不响应
            return None

        return WxBotHelper.get_res_xml(from_user_id, res_content)

    @classmethod
    def _clear_outdated_showed_tip_buffer(cls, s_today):
        """清理掉 s_today 之前的记录，使得缓存中只保留当天的记录"""
        items_to_remove = []
        for item in cls.just_showed_tip_buffer:
            if item[1] != s_today:
                items_to_remove.append(item)
        for item in items_to_remove:
            cls.just_showed_tip_buffer.remove(item)

    @classmethod
    def _report_bug(cls, from_user_id, content):
        # 用户发送提bug确认消息，并且 bug 信息已在缓存中。直接提 bug
        if content == WxBotConf.BUG_ENSURE_KEY and from_user_id in cls.report_buffer:
            return cls._do_report_bug(from_user_id)

        if not WxBotHelper.contain_keywords(content):
            if from_user_id in cls.report_buffer:
                del cls.report_buffer[from_user_id]
            # 开启图灵机器人闲聊模式
            return TuringBot.ask_turing_bot(content)

        # 如果只有关键字，给出非法提示
        if re.sub(r'[^\w\s]', '', content) in WxBotConf.BUG_KEY_WORDS:
            return WxBotConf.INVALID_CONTENT_TIP

        return cls._cache_bug_info_and_ask_for_ensure(content, from_user_id)

    @classmethod
    def _cache_bug_info_and_ask_for_ensure(cls, content, from_user_id):
        jira_username = WxBotHelper.get_jira_username_by_wx_userid(from_user_id)
        summary, desc = WxBotHelper.parse_summary_and_desc_from_content(content)
        bug_info = {'jira_username': jira_username, 'summary': summary, 'desc': desc}
        logging.info("监测到bug关键词，生成信息如下：" + str(bug_info))
        # 将bug信息放入缓存中，提醒用户确认
        cls.report_buffer[from_user_id] = bug_info
        result = WxBotConf.BUG_ENSURE_TEMPLATE.format(jira_username, summary, desc)
        return result

    @classmethod
    def _do_report_bug(cls, from_user_id):
        bug_info = cls.report_buffer[from_user_id]
        logging.info("已确认，开始提bug：" + str(bug_info))
        result = CrmBugHelper.report_bug(bug_info['jira_username'], bug_info['summary'], bug_info['desc'])
        del cls.report_buffer[from_user_id]
        if 'key' in result:
            # 提交成功的情况
            bug_num = result['key']
            WxBotHelper.send_bug_success_feedback(bug_num, from_user_id, bug_info)
            return "欢迎下次再来～"
        error_tip = result['errors'] if 'errors' in result else result
        name_tip = "很可能你的微信用户名与JIRA用户名不匹配。\n" if 'errors' in result and 'reporter' in result['errors'] else ''
        return "提 BUG 过程出现异常：\n{}\n\n{}请联系机器人开发者。\n".format(error_tip, name_tip)

