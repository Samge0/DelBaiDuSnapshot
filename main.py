#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2020/12/27 下午3:20
# @Author  : Samge

import time
from enums import *
from setting import *
from utils import baidu_snapshot_manager, file_util

"""
自动提交百度快照申诉的脚本

这个页面是有提交频率限制的，我手动提交过于频繁（大概 5-10 秒一次，提交 5 个左右）就会提示让你歇一会
"""


if __name__ == '__main__':
    start = time.time()
    for shot_info in baidu_snapshot_manager.get_baidu_results(keyword=KEYWORD):
        print('\n\n开始处理快照： {}'.format(shot_info))
        shot_title = shot_info[0]
        shot_url = shot_info[1]
        status_code = baidu_snapshot_manager.del_baidu_snapshot(shot_title=shot_title, shot_url=shot_url, retry_times=RETRY_TIMES)
        if status_code == StatusCode.ERROR_LOGIN.value:
            break
        elif status_code == StatusCode.ERROR_VCODE.value:
            print('验证码错误次数超过{}次，url= {}'.format(RETRY_TIMES, shot_url))
            file_util.save_txt_file('{}\n'.format(shot_url), FILE_TOUSU_ERROR, 'a+')
        elif status_code != StatusCode.EXIST.value:
            print('\n\n休眠{}秒后继续执行任务'.format(TIME_SLEEP))
            time.sleep(TIME_SLEEP)
    print('总任务执行完毕，耗时共: {} 秒'.format(time.time() - start))
