#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2020/12/27 下午3:20
# @Author  : Samge

# 【*必要配置】打码平台的账号密码，需要配置为自己的账号密码 (这里验证码识别用的是[图鉴](http://www.ttshitu.com/))
USER_NAME = ''
USER_PW = ''

# 【*必要配置】百度搜索中的关键词
KEYWORD = ''

# 【*必要配置】百度账号登录后的cookie信息，这里是手动配置，过期后需要重新获取替换（登录百度账号之后，打开快照页面（http://help.baidu.com/newadd?prod_id=212），复制请求头中的Cookie完整值）
COOKIE = ''

# 快照列表过滤关键词，多个关键词要用|符号隔开，允许为空
SNAPSHOT_FILTER_KEY = ''

# user-agent
USER_AGENT = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'

# 验证码失败重试次数/提示申诉频繁重试次数，共用该参数
RETRY_TIMES = 5

# 提交一个申诉的间隔时间，间隔太短会提示操作频繁，这个时间根据实际情况调整（有多个百度账号的话可以调低 & 修改代码），默认间隔2分钟(经测试，2分钟间隔很少提示操作频繁，原先试过1分钟间隔会经常提示)
TIME_SLEEP = 2 * 60

# 提交一个申诉后提示操作频繁的休眠时间，默认间隔3分钟
TIME_SLEEP_FREQUENT = 3 * 60

# 成功提交申诉的记录，避免重复操作
FILE_TOUSU_COMMIT_SUCCEED = 'tousu_commit_succeed.txt'

# 【验证码多次获取失败/检验失败/多次提示申诉请求频繁导致失败】的记录
FILE_TOUSU_ERROR = 'tousu_error.txt'

