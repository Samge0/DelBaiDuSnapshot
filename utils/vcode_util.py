#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2020/12/27 上午11:09
# @Author  : Samge

import base64
import json
import requests
import setting


"""验证码识别工具, 使用第三方识别服务"""


def get_vcode_result(vcode_img_path, vcode_msg, retry_times):
    """
    识别认证码，返回坐标信息
    :vcode_img_path: 需要点击验证的验证码图片地址
    :vcode_msg: 需要点击的文字信息
    :retry_times: 验证码重试次数/提示申诉频繁重试次数
    """
    if setting.USER_NAME is None or len(setting.USER_NAME) == 0:
        raise ValueError('验证码识别的账号&密码不能为空，请在setting.py中配置')
    api_url = 'http://api.ttshitu.com/imageXYPlus'
    b64 = to_base64(vcode_img_path)
    typeid = 20
    data = {"username": setting.USER_NAME, "password": setting.USER_PW, "image": b64, "typeid": typeid, "remark": vcode_msg}
    result = json.loads(requests.post(api_url, json=data).text)
    print(result)
    if result['success']:
        return result["data"]["result"].split('|'), result["data"]["id"]

    _times = retry_times - 1
    if _times > 0:
        print('验证码解析失败，需要重新获取验证码')
        return get_vcode_result(vcode_img_path, vcode_msg, retry_times=_times)

    return None, None


def to_base64(img):
    """获取图片的base64"""
    b64 = ''
    with open(img, 'rb') as f:
        base64_data = base64.b64encode(f.read())
        b64 = base64_data.decode()
    return b64


def report_error(vcode_id):
    """
    验证码识别错误时进行上报
    :vcode_id: 验证码识别结果返回的id
    """
    if vcode_id is None:
        print("验证码vcode_id为空，上报信息取消")
        return
    data = {"id": vcode_id}
    result = json.loads(requests.post("http://api.ttshitu.com/reporterror.json", json=data).text)
    print('验证码识别错误上报结果：' + str(result))
    if result['success']:
        print("验证码识别错误，上报信息成功")
    else:
        print("验证码识别错误，上报信息失败")
        print(result["message"])
