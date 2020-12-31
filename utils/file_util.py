#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2020/12/27 下午3:20
# @Author  : Samge

import os
import random
from urllib.parse import parse_qsl

import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


def save_txt_file(_txt, _path, _type='w+'):
    """保存文件"""
    try:
        with open(_path, _type) as f:
            f.write(_txt)
            f.flush()
            f.close()
    except Exception as e:
        print(e)
        pass


def read_txt_file(_path):
    """读取文件"""
    if os.path.exists(_path) is False:
        return None
    with open(_path, "r", encoding='utf-8') as f:  # 打开文件
        data = f.read()
        f.close()
        if data == '':
            return None
        else:
            return data


def read_txt_file_random_line(_path):
    """读取文件某一行"""
    if os.path.exists(_path) is False:
        return None
    with open(_path, "r") as f:  # 打开文件
        lines = f.readlines()
        return lines[random.choice([i for i in range(len(lines))])]


def read_txt_file_line(_path, curr_line):
    """读取文件某一行"""
    if os.path.exists(_path) is False:
        return None
    with open(_path, "r") as f:  # 打开文件
        lines = f.readlines()
        if curr_line < len(lines):
            return lines[curr_line]
        else:
            return None


def read_txt_file_scope(_path, start_line=None, end_line=None):
    """读取文件某一段区间内容"""
    try:
        if os.path.exists(_path) is False:
            return None
        with open(_path, "r") as f:  # 打开文件
            lines = f.readlines()
            if start_line is None:
                start_line = 0
            if end_line is None:
                end_line = len(lines)
            return lines[start_line: end_line]
    except Exception as e:
        print(e)
        return None


def save_txt_file_scope(_path, start_line=None, end_line=None):
    """仅保存某一段区间内容"""
    try:
        if os.path.exists(_path) is False:
            return None
        _txt = ''
        with open(_path, "r") as f:  # 打开文件
            lines = f.readlines()
            if start_line is None:
                start_line = 0
            if end_line is None:
                end_line = len(lines)
            _txt = ''.join(lines[start_line: end_line])
        print(_txt)
        with open(_path, "w") as f:  # 打开文件
            f.write(_txt)
            f.flush()
            f.close()
    except Exception as e:
        print(e)
        return None


def read_txt_file_lines(_path):
    """读取文件行数"""
    # 文件比较小
    if os.path.exists(_path) is False:
        return 0
    return len(open(_path, 'rU').readlines())


def get_ocname_keys(_path=None):
    """读取公司关键词"""
    if _path is None:
        _path = '../ocname_keys.txt'
    result = read_txt_file(_path) or ''
    return result.split('\n')


def get_file_ext(file_name):
    """通过split方式获取文件扩展名"""
    if file_name and '.' in file_name:
        _split = file_name.split('.')
        return _split[len(_split) - 1]
    return None


def get_file_name_from_disposition(content_disposition):
    """
    从响应头的Content-Disposition中读取文件名

    例如：
    'form-data; name=file;filename=test.txt;'
    'attachment;filename=xxx.doc'
    """
    if content_disposition is None:
        return None
    if type(content_disposition) is bytes:
        content_disposition = str(content_disposition, encoding="utf-8")
    if type(content_disposition) is not str:
        raise ValueError('传入的参数需要字符串类型')
    _d = dict(parse_qsl(content_disposition))
    return _d.get('filename')

