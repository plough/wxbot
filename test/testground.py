#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
 本文件没有实际作用，直接删除是没问题的。
 开发时，可以在这里做一些 api 试验。
 Created by plough on 2018/11/16.
"""
# from bs4 import BeautifulSoup
from xml.etree import ElementTree as ET


def main():
    # WxBot.send_msg_to_group("太阳当空照，花儿对我笑")
    # WxBot.get_msg(None)
    xml = "<xml><ToUserName><![CDATA[ww1cfe92ce0552bbe8]]></ToUserName><FromUserName><![CDATA[qy01d035f0f8b128079cdb97d5bc]]></FromUserName><CreateTime>1542359914</CreateTime><MsgType><![CDATA[text]]></MsgType><Content><![CDATA[777]]></Content><MsgId>482458336</MsgId><AgentID>1000036</AgentID></xml>"
    root = ET.XML(xml)
    from_user_name = root.find('FromUserName').text
    content = root.find('Content').text
    print(from_user_name, content)

if __name__ == '__main__':
    main()