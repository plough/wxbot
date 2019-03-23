# 企业微信提bug机器人开发文档

> 建议结合本文档和单元测试一起阅读


## 1. 功能简介
#### 1.1 提 crm bug
这是目前唯一的实用功能。
细分如下：
1. 监听打开对话框事件，发送欢迎消息
2. 检测关键词，向用户二次确认后，提 crm bug 到 JIRA 系统
3. 向用户返回结果（成功或失败的提示）
4. 如果提交成功，向机器人全员通知群，发一条卡片消息，包含 bug 的摘要。点击卡片可以跳转 JIRA 任务详情页面
#### 1.2 聊天机器人
除了跟它聊天斗嘴，还可以查天气，讲笑话。

![](images/%E4%BC%81%E4%B8%9A%E5%BE%AE%E4%BF%A1%E6%8F%90bug%E6%9C%BA%E5%99%A8%E4%BA%BA%E5%8A%9F%E8%83%BD%E5%9B%BE.png)

## 2. 相关技术点提要
语言是 Python3，服务器框架为 Flask。
- 日志系统为 python 内置的日志模块
- 加密/解密：微信官方提供的工具类
- XML 解析：python 内置模块
- 企业微信交互：微信官方提供的 api 封装类
- 网络请求：requests 库
- 提 bug：参考 crm 的 Java 代码，分析出给 JIRA 提 bug 的 api，然后用 requests 库发送 http 请求
- 闲聊：图灵机器人接口

## 3. GettingStarted
#### 3.1 开发环境搭建
1. 把项目源码 clone 到本地
2. 安装 Python3，安装相关依赖包（`pip install -r requirements.txt`），安装 PyCharm
3. 用 PyCharm 打开 wxbot 目录
4. 运行 `run_server.py`，启动服务器，一切就绪（本地运行意义不大）
5. 阅读或运行已经写好的单元测试，快速熟悉代码
#### 3.2 部署运行
1. 将整个项目传到服务器上（压缩，scp上传，再解压）
2. 安装 Python3（参考[http://baimoz.me/1687/](http://baimoz.me/1687/)），安装相关依赖包（`pip install -r requirements.txt`）（pip 可能需要改为 pip3，具体看服务器上是怎么配置的）
3. 检查 `config.py` 中的配置项
4. 运行 `run_server.sh`，启动服务器（加了一层封装，内部还是执行 `run_server.py`）
5. 浏览器访问服务器地址，检查是否启动成功
6. 初次使用，或者迁移服务器，需要配置企业微信后台

#### 3.3 额外提示
##### 3.3.1 如何在后台运行程序？
`nohup ./run_server.sh &`
##### 3.3.2 如何终止后台运行的程序？
1. 查看后台进程，找到 wxbot 对应的进程号（pid）
2. `kill {pid}`
##### 3.3.3 可以把上传到服务器的步骤，封装为 sh 脚本
参考：
```bash
#!/bin/bash

fname=wxbot.tar.gz
dname=wxbot

rm $fname
tar -cvzf $fname $dname
scp $fname root@xx.xxx.xx.xx:~/ # 替换为真实的 ip 地址
```
服务器上的解压命令为 `tar -xvzf wxbot.tar.gz`。

## 4. 项目目录结构
![](images/%E5%BE%AE%E4%BF%A1%E6%9C%BA%E5%99%A8%E4%BA%BA%E9%A1%B9%E7%9B%AE%E7%BB%93%E6%9E%84%E5%9B%BE.png)

## 5. 基本运维思路
#### 5.1 文案修改、名字映射修改、第三方接口配置修改
统一修改 `config.py`。改完之后，重新运行一下。
#### 5.2 端口号修改
在 `run_server.py` 中修改。注意要同时修改企业微信后台的地址。
#### 5.3 新增 bug 类型
1. 扩展 jiraapi 包的功能（如果是 crm 已经有的功能，可以跟信息组要一下 java 文件，看接口怎么调用的）。
2. 从 `WxBot.make_response` 入手，添加业务功能
#### 5.4 聊天表情
1. 研究企业微信的 api（[https://work.weixin.qq.com/api/doc#90000/90135/90664](https://work.weixin.qq.com/api/doc#90000/90135/90664)）
2. 从 `WxBot.make_response` 入手，增加相应逻辑
#### 5.5 调试，改bug
1. 优先看 wxbot.log 文件（运行过程中会生成）。
2. 本地用 PyCharm 调试，调好之后上传到服务器。杀掉原来的服务，并删除老的文件夹。再次启动服务器。
3. 如果本地调试不方便的，在代码里加 log，再调试

## 6、可能存在的坑点
- 并发风险（目前都是用的静态方法和类方法）
- 未使用正式的服务器（Flask 内置服务器，性能不好，只适合调试用。但是运行至今也没发现啥问题，所以懒得改了。后期可能需要切换到正式的服务器（cgi + 反代啥的，Flask 官网有教程））
- 其他的还没想到，碰到再说吧，超出新手村范围了
