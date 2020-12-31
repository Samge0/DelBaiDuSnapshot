#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2020/12/27 下午3:10
# @Author  : Samge

from enum import Enum


# 提交百度快照申诉的结果状态码
class StatusCode(Enum):
    SUCCEED = 0  # 操作成功
    ERROR_VCODE = 5  # 验证码失败
    ERROR_LOGIN = 6  # 未登录
    FREQUENT = 7  # 操作频繁
    EXIST = 11  # 记录已存在
    ERROR_OTHER = 10000  # 其他错误
    ERROR_SUBMIT_TOKEN = 10001  # submit_token解析失败
