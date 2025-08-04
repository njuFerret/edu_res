#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   suanshuti.py
@Time    :   2025/06/20 16:44:03
@Author  :   Ferret@NJTech
@Version :   1.0
@Contact :   Ferret@NJTech
@License :   (C)Copyright 2025, Ferret@NJTech
@Desc    :   补充描述
'''

from datetime import datetime
import logging
import pathlib
import requests
from lxml import etree

START = datetime.now()
thisScript = pathlib.Path(__file__)
logLevel = logging.INFO

title = 'None'
type_cal = 7        # 计算类型, 1:加法,2:减法, 3:加减混合, 4:乘法, 5:除法, 6:乘除混合, 7:混合运算

cal_num = 4         # 数字个数, 测试20成功
max_num = 100        # = 最大数字
with_bracket = 1    # 1:带括号, 0:不带括号

num_per_page = 40   # 分页数量
total_number = 400  # 题目总数, 测试800题 PASS

type_cals = ['加法','减法', '加减混合', '乘法', '除法', '乘除混合', '混合四则']
title = f'{type_cals[(type_cal -1) % 7]}运算'

if cal_num == 2:
    with_bracket=0


title = f'{title}({max_num}以内)'

logFileName = f"{title}_{datetime.now().strftime('%Y%m%d-%H%M%S')}.log"
logFile = thisScript.with_name(logFileName)
#logFile = thisScript.with_suffix('.log')

# fmt:off
# Basic logging configuration
logging.basicConfig(
    level=logLevel,
    format='%(message)s' if logLevel == logging.INFO else '%(asctime)s %(filename)s(%(lineno)04d) [%(levelname)-8s]: %(message)s',
    handlers=[logging.FileHandler(logFile, mode='w', encoding='utf-8'), logging.StreamHandler()],
    datefmt='%Y-%m-%d %H:%M:%S'
)
# fmt:on
logger = logging.getLogger(__name__)



def getQuestions():
    sess = requests.session()

    proxies = {
        'http': 'http://jpoffice_v4:33080',
        'https': 'http://jpoffice_v4:33080',
    }

    url = 'https://www.an2.net/cal/zi.php'

    payload = {
        'num_type': '1',            # 数字类型, 1:整数, 2:小数    
        'max': max_num-1,           # 最大数字
        #'max': '99',
        'type_cal': type_cal,       # 计算类型, 1:加法,2:减法, 3:加减混合, 4:乘法, 5:除法, 6:乘除混合, 7:混合运算
        'cal_num': cal_num,         # 数字个数
        'bracket': with_bracket,    # 括号，1:带括号, 0:不带括号
        'positive_num': '1',        # 1: 结果强制非负, 0: 结果可负
        'int_num': '1',             # 1: 结果强制为整数, 0: 结果可非整
        'num': total_number,        # 题目数量
        'tzgbt': title,             # 标题
    }

    r = sess.post(url, data=payload, proxies=proxies)

    html = etree.HTML(r.text)

    questions = html.xpath('//ul/li/text()')

    questions = [q.replace(' ', '').strip().replace('=', ' =') for q in questions]
    questions = [f"{q[:-2]}{' '*(17-len(q))} =" for q in questions]

    return questions


def getAnswer(questions):
    msg = ''
    today = datetime.now().strftime('%Y年%m月%d日')    
    total_pages = len(questions)/num_per_page
    for idx, s in enumerate(questions):
        if idx % 2 == 0:
            if idx % num_per_page == 0:
                page_index = idx//num_per_page
                msg = f'{today} {title} ( {page_index + 1:02d}/{total_pages:2.0f} )\n'
            else:
                msg = ''
            msg += f'[{idx+1:03d}] {s}'
            msg += f"{(eval(s.replace('=', '').replace('÷','/').replace('x','*'))):.0f}" #str(eval(s.replace('=', '')))
        else:
            msg += '\t\t\t\t\t'
            msg += f'[{idx+1:03d}] {s}'
            msg += f"{(eval(s.replace('=', '').replace('÷','/').replace('x','*'))):.0f}"
            if (idx + 1) > 10 and (idx + 1) % num_per_page == 0:
                msg += "\n\n"
            logger.info(msg)
    logger.info('\n\n')


def forPrint(questions):
    msg = ''
    today = datetime.now().strftime('%Y年%m月%d日')    
    total_pages = len(questions)/num_per_page
    for idx, s in enumerate(questions):
        if idx % 2 == 0:
            if idx % num_per_page == 0:
                page_index = idx//num_per_page
                msg = f'{today} {title} ( {page_index + 1:02d}/{total_pages:2.0f} )\n'
            else:
                msg = ''
            msg += f'[{idx+1:03d}] {s}'
        else:
            msg += '\t\t\t\t\t'
            msg += f'[{idx+1:03d}] {s}'
            if (idx + 1) > 10 and (idx + 1) % 40 == 0:
                msg += "\n\n"
            logger.info(msg)
    logger.info('\n\n')


def main():

    q = getQuestions()
    logger.info('\n\n')
    forPrint(q)
    getAnswer(q)


if __name__ == '__main__':
    # fmt: off
    #logger.info('脚本 %s 开始运行, 时间：%s ' %(thisScript.name, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
    main()
    #logger.info('脚本 %s 运行完成, 时间：%s ' %(thisScript.name, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
    # fmt: on
