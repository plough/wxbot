#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
 所有配置都放在这个文件里，统一管理。
 本来想上 yaml 的，转念一想，配置较少，没必要搞那么复杂。以后有需要再重构吧。
 Created by plough on 2018/11/16.
"""

# 设置为true会打印一些调试信息，上线时可以关闭
DEBUG = True


"""
 业务逻辑相关配置
"""
class WxBotConf:
    """提bug机器人所在的讨论组的id，一般情况下不需要改动"""
    CHAT_ID = 'wxbot0crmbug0group'

    """用户名映射（企业微信->JIRA）"""
    WX_JIRA_NAME_MAP = {
        'Ziv': 'Ziv.Zhang',
        'Zhonglin': 'Zhonglin.Pei',
    }

    """提bug的关键词"""
    BUG_KEY_WORDS = "crm,CRM,Crm,问题,异常,bug,BUG,Bug,挂了,炸了,崩了,报错,打不开".split(',')

    """各种提示"""
    FIRST_USE_TIP = "欢迎帮助我们找出产品bug😊\n请尽量一次性将问题描述完整，切勿分开发送！"
    INVALID_CONTENT_TIP = "请尽量一次性将问题描述完整，切勿分开发送！😊"
    BUG_ENSURE_KEY = "1"
    BUG_ENSURE_TEMPLATE = "以下是您本次所提交BUG，请予以确认！\n回复 %s 正式提交此BUG，回复其它任何内容取消提交。\n报告人：{}\n标题：{}\n描述：{}" % BUG_ENSURE_KEY
    # 发送给个人的 BUG 提交消息模版
    # TODO: 修改链接里的 url
    BUG_REPORT_INFO_USER = "BUG创建成功，稍后会有相关人员与您联系了解此BUG详细信息。请保持联系畅通😊\nBUG编号：<a href='http://www.pleasechangethis.com:6006/browse/{0}'>{0}</a>"
    CARD_MSG_TITLE = "BUG通知"
    # 群聊 BUG 提交消息模版（正文部分）
    BUG_REPORT_INFO_GROUP = "由{}提交 {}\n标题：{}\n描述：{}"
    # 限制卡片消息的长度
    MAX_GROUP_DESC_WORD_NUMBER = 45
    # BUG 跳转链接模版（TODO: 修改为自己JIRA服务器的任务地址）
    BUG_URL_TEMPLATE = "http://www.pleasechangethis.com:6006/browse/{}"
    # 错误提示模版
    REPORT_BUG_ERROR_TIP = "提 BUG 过程出现异常：\n{}\n\n很可能你的微信用户名与JIRA用户名不匹配。\n请联系机器人开发者。\n"


"""
 api 相关配置，一般情况下不需要改动
"""
# Turing API 配置
class TuringConf:
    URL = 'http://openapi.tuling123.com/openapi/api/v2'
    # TODO: 修改为自己的接口配置
    API_KEY = 'xxxxxxxx'
    USER_ID = 'xxxxxx'


# crm 配置
class CrmConf:
    # TODO: 修改 JIRA 服务器的地址和管理员账号信息
    ADD_ISSUE_URL = 'http://www.pleasechangethis.com:6006/rest/api/2/issue/'
    ADMIN_NAME = 'crm'
    ADMIN_PASSWORD = 'password111'


# 企业微信配置
class WxConf:
    # 企业的id，在管理端->"我的企业" 可以看到
    # TODO: 更换为自己的ID
    CORP_ID = "xxxxxxxx"

    # 某个自建应用的id及secret, 在管理端 -> 企业应用 -> 自建应用, 点进相应应用可以看到
    # TODO: 修改为自己的 APPID 和 APP SECRET
    APP_ID = 1000006
    APP_SECRET = "ABCDEFGXXXxxxxXXXxxx"

    # 接收消息服务器配置
    # TODO: 修改为自己的 token 和 key
    APP_TOKEN = "xxXXXxxxXXXX"
    APP_ENCODING_AES_KEY = "xx31xxxxXXX"
