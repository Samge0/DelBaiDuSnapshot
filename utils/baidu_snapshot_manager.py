#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2020/12/27 上午11:21
# @Author  : Samge

import os
import json
import time
import random
import requests
from enums import *
from setting import *
from urllib import parse
from utils import file_util, vcode_util
from requests_html import HTMLSession, HTML


"""
删除百度快照的工具
"""


# 初始化requests_html对象
session = HTMLSession()

# 通用请求头
HEADERS_COMMON = {
    'User-Agent': USER_AGENT,
}

URL_BAIDU_QUERY_LIST = 'https://www.baidu.com/s?ie=utf-8&f=8&rsv_bp=1&tn=baidu&wd={keyword}&pn={index}'  # 百度查询结果列表，GET
URL_TOUSU = 'http://help.baidu.com/newadd?prod_id=1&category=1&link={link}'  # 百度快照投诉链接详情页，GET
URL_VCODE_IMG = 'http://help.baidu.com/getcodeimage?0.{}'  # 验证码图片获取地址，GET
URL_VCODE_MSG = 'http://help.baidu.com/getcodetext'  # 验证码需要点击的文字，需要在获取验证码图片后调用，GET
URL_TOUSU_COMMIT = 'http://help.baidu.com/toususubmit'  # 百度快照申诉的提交地址，POST

# 百度快照提交申诉的请求体模板
# webmaster_typen 内容可选：网页打不开或者内容已删除，无法找到该网页 or 搜索内容和实际不一致
BODY_DICT = {
    'os_info': 'Macintosh',
    'browser_info': 'chrome 85',
    'client_version': '',
    'pid': '1',
    'category_id': '1',
    'title': '快照删除与更新',
    'content': '快照删除与更新',
    'webmaster_type': '搜索内容和实际不一致',
    'email': ''
  }


def get_baidu_results(keyword):
    """获取符合要求的百度快照链接"""

    if keyword is None or keyword == '':
        raise ValueError('参数keyword不能为空，请在setting.py中配置')

    LIMIT = 10
    url = URL_BAIDU_QUERY_LIST.format(keyword=keyword, index=0)
    r = session.get(url)
    max_page = int(r.html.find('.pc')[1].text)
    print('总页数：：{}'.format(max_page))

    shot_info_list = []
    for i in range(max_page):
        index = i * LIMIT
        url = URL_BAIDU_QUERY_LIST.format(keyword=keyword, index=index)
        r = session.get(url)
        for _div in r.html.find('.user-avatar'):
            if check_shot_filter(_div.text) is True:
                for url in list(_div.absolute_links):
                    if 'cache.baiducontent.com' in url:
                        shot_title = get_shot_title(HTML(html=_div.html))
                        shot_info_list.append((shot_title, url))
    return shot_info_list


def check_shot_filter(value):
    """检测是否符合快照过滤规则"""
    if value is None:
        return False
    if SNAPSHOT_FILTER_KEY is None or SNAPSHOT_FILTER_KEY == '':
        return True
    for item in SNAPSHOT_FILTER_KEY.split('|'):
        if item in value:
            return True
    return False


def get_shot_title(_html):
    """
    获取快照的标题
    :_html: 当前快照div对应的HTML对象
    """
    try:
        return json.loads(_html.find('.c-tools', first=True).attrs['data-tools']).get('title')
    except:
        return None


def get_vcode_info(url_tousu, cookies):
    """获取验证码的图片 & 需要点击的文字 信息"""
    headers = HEADERS_COMMON
    headers['Referer'] = url_tousu

    vcode_img_name = str(time.time() + random.randint(1, 100000)).replace('.', '')
    vcode_img_path = 'imgs/{}.png'.format(vcode_img_name)
    url_vcode_img = URL_VCODE_IMG.format(vcode_img_name)
    r_img = requests.get(url_vcode_img, headers=headers, cookies=cookies)
    file_util.save_txt_file(r_img.content, vcode_img_path, 'wb')
    vcode_tracecode = r_img.headers.get('Tracecode')

    vcode_msg = requests.get(URL_VCODE_MSG, headers=headers, cookies=cookies).text
    vcode_msg = '，'.join(eval(vcode_msg.encode('utf8').decode('unicode_escape')))
    print('{}\n{}\n{}'.format(vcode_img_path, vcode_msg, vcode_tracecode))
    return vcode_img_path, vcode_msg, vcode_tracecode


def get_cookies():
    """提取cookies"""

    if COOKIE is None or COOKIE == '':
        raise ValueError('参数cookie不能为空，请在setting.py中配置')

    cookies = {}
    for cookie in COOKIE.replace('; ', ';').split(';'):
        _splits = cookie.split('=')
        cookies[_splits[0]] = _splits[1]
    print(cookies)
    return cookies


def get_submit_token(cookies):
    """提取submit_token"""
    submit_token = None
    r = session.get(URL_TOUSU, headers=HEADERS_COMMON, cookies=cookies)
    for _input in r.html.find('input') or []:
        if 'submit_token' in str(_input):
            submit_token = _input.attrs['value']
            print('submit_token = {}'.format(submit_token))
    return submit_token


def get_commit_body(shot_url, submit_token, vcode_results):
    """
    获取提交申诉的请求体
    :shot_url: 百度快照链接
    :submit_token: 提交时用到的token，快照提交的html页面中可提取到
    :vcode_results: 验证码识别成功返回的坐标列表
    """
    body_dict = BODY_DICT
    body_dict['links[]'] = shot_url
    body_dict['submit_token'] = submit_token
    for i in range(len(vcode_results)):
        result = vcode_results[i]
        _splits = result.split(',')
        body_dict['verify_code[{}][x]'.format(i)] = int(_splits[0])
        body_dict['verify_code[{}][y]'.format(i)] = int(_splits[1])
    body_dict = parse.urlencode(body_dict)
    print('请求体：{}'.format(body_dict))
    return body_dict


def get_commit_headers(vcode_tracecode):
    """
    获取提交申诉的请求头
    :vcode_tracecode: 获取验证码后返回的 Tracecode
    """
    headers = HEADERS_COMMON
    headers['Tracecode'] = vcode_tracecode
    headers['Content-Type'] = 'application/x-www-form-urlencoded'
    print('请求头：{}'.format(headers))
    return headers


def do_commit(**kwargs):
    """
    提交百度快照申诉
    :kwargs: Optional arguments that ``request`` takes.

    百度快照申诉返回结果示例：
    {errno: 0, errmsg: "反馈成功<br>感谢您的关注和支持！"}
    {"errno":5,"errmsg":"点选验证码-参数提交错误"}
    {'errno': 6, 'errmsg': '您还没有登录，请先登录。'}
    {"errno":7,"errmsg":"请不要在短时间内连续发起反馈。休息一下，稍后再试~"}
    {errno: 11, errmsg: "请不要针对同一问题重复进行举报，我们会尽快处理，并通过百度账号下发给您。"}
    """
    result = requests.post(URL_TOUSU_COMMIT, **kwargs)
    result_text = result.text or ''
    status_code = None
    try:
        print('提交百度申诉结果：{}'.format(result_text.encode('utf8').decode('unicode_escape')))
        result = json.loads(result_text)
        status_code = result.get('errno')
    except Exception as e:
        print('解析结果失败：{}'.format(e))

    return status_code


def del_baidu_snapshot(shot_title, shot_url, retry_times=None):
    """
    提交删除百度快照的请求
    :shot_title: 百度快照标题
    :shot_url: 百度快照链接
    :retry_times: 验证码重试次数/提示申诉频繁重试次数
    """
    start = time.time()

    if retry_times is None:
        retry_times = RETRY_TIMES

    if shot_url is None or shot_url == '':
        raise ValueError('参数shot_url不能为空')

    tousu_succeed_txt = file_util.read_txt_file(FILE_TOUSU_COMMIT_SUCCEED)
    if tousu_succeed_txt and shot_title in tousu_succeed_txt:
        print('该链接已经提交百度处理，跳过：{}\n{}'.format(shot_title, shot_url))
        return StatusCode.EXIST.value

    print('\n正在提取cookies')
    cookies = get_cookies()

    print('\n正在获取submit_token')
    submit_token = get_submit_token(cookies=cookies)
    if submit_token is None:
        print('submit_token获取失败，跳过：{}'.format(submit_token))
        return StatusCode.ERROR_SUBMIT_TOKEN.value

    print('\n正在获取验证码图片相关信息')
    vcode_img_path, vcode_msg, vcode_tracecode = get_vcode_info(url_tousu=URL_TOUSU.format(link=shot_url), cookies=cookies)

    print('\n正在调用api获取验证码的点击坐标信息')
    vcode_results, vcode_id = vcode_util.get_vcode_result(vcode_img_path=vcode_img_path, vcode_msg=vcode_msg, retry_times=retry_times)
    if vcode_results is None or vcode_id is None:
        return StatusCode.ERROR_VCODE.value

    print('\n正在提交百度申诉')
    body_dict = get_commit_body(shot_url=shot_url, submit_token=submit_token, vcode_results=vcode_results)
    headers = get_commit_headers(vcode_tracecode=vcode_tracecode)
    status_code = do_commit(headers=headers,
                            data=body_dict,
                            cookies=cookies)

    if status_code == StatusCode.SUCCEED.value or status_code == StatusCode.EXIST.value:
        file_util.save_txt_file('{}\n{}\n\n'.format(shot_title, shot_url), FILE_TOUSU_COMMIT_SUCCEED, 'a+')
        print('百度快照申诉已成功提交')
    elif status_code == StatusCode.FREQUENT.value:
        print('被检测到请求频繁，睡眠{}秒后再继续任务'.format(TIME_SLEEP_FREQUENT))
        time.sleep(TIME_SLEEP_FREQUENT)
        _times = retry_times - 1
        if _times > 0:
            print('前面操作被检测到请求频繁，现重新提交申诉')
            return del_baidu_snapshot(shot_title=shot_title, shot_url=shot_url, retry_times=_times)
    elif status_code == StatusCode.ERROR_VCODE.value:
        vcode_util.report_error(vcode_id)
        _times = retry_times - 1
        if _times > 0:
            print('验证码校验失败，需要重新获取验证码')
            return del_baidu_snapshot(shot_title=shot_title, shot_url=shot_url, retry_times=_times)
    elif status_code == StatusCode.ERROR_LOGIN.value:
        print('登录状态失效，退出当前任务循环，请手动更新Cookies后继续')

    os.remove(vcode_img_path)

    print('任务执行完毕，耗时共: {} 秒'.format(time.time() - start))
    return status_code
