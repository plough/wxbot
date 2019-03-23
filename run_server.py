#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
 机器人服务器入口文件
 Created by plough on 2018/11/16.
"""
import sys
from flask import Flask, request

import config
from app.utils.wxbot_helper import WxBotHelper
from app.wxbot import WxBot

app = Flask(__name__)

@app.route("/wxbot", methods=['GET', 'POST'])
def hello():
    # token 验证，只进行一次。验证成功后，以后都不再发送此请求
    if request.method == 'GET' and 'echostr' in request.args:
        reply_echo_str = WxBotHelper.verify_url(request.args)
        return reply_echo_str

    # 正常接收消息
    if request.method == 'POST':
        encrypt_msg = answer_msg_and_encrypt(request.args, request.get_data(as_text=True))
        return encrypt_msg


def init_logging():
    import logging
    logging.basicConfig(
        filename='wxbot.log',
        format='%(asctime)s %(levelname)s: %(message)s',
        datefmt='%Y/%m/%d %H:%M:%S',
        level=logging.DEBUG)


def answer_msg_and_encrypt(args, encrypt_xml_data):
    s_msg_signature = args['msg_signature']
    s_timestamp = args['timestamp']
    s_nonce = args['nonce']

    s_xml_content = WxBotHelper.decrypt_msg(s_msg_signature, s_timestamp, s_nonce, encrypt_xml_data)

    s_res_xml = WxBot.make_response(s_xml_content)
    if s_res_xml is None:
        sys.exit(0)

    return WxBotHelper.encrypt_msg(s_res_xml, s_nonce, s_timestamp)


if __name__ == "__main__":
    init_logging()
    app.run(host="0.0.0.0", port=5006, debug=config.DEBUG)
