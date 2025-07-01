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
logFile = thisScript.with_suffix('.log')

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
        'num_type': '1',
        'max': '49',
        'type_cal': '3',
        'cal_num': '4',
        'bracket': '1',
        'positive_num': '1',
        'int_num': '0',
        'num': '400',
        'tzgbt': '加减混合运算',
    }

    r = sess.post(url, data=payload, proxies=proxies)

    html = etree.HTML(r.text)

    questions = html.xpath('//ul/li/text()')

    questions = [q.replace(' ', '').strip().replace('=', ' =') for q in questions]
    questions = [f"{q[:-2]}{' '*(17-len(q))} =" for q in questions]

    return questions


def getAnswer(questions):
    msg = ''
    for idx, s in enumerate(questions):
        if idx % 2 == 0:

            msg = f'[{idx+1:03d}] {s}'
            msg += str(eval(s.replace('=', '')))
        else:
            msg += '\t\t\t\t\t'
            msg += f'[{idx+1:03d}] {s}'
            msg += str(eval(s.replace('=', '')))
            if (idx + 1) > 10 and (idx + 1) % 40 == 0:
                msg += "\n\n"
            logger.info(msg)
    logger.info('\n\n')


def forPrint(questions):
    msg = ''
    for idx, s in enumerate(questions):
        if idx % 2 == 0:
            msg = f'[{idx+1:03d}] {s} '
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
    logger.info('脚本 %s 开始运行, 时间：%s ' %(thisScript.name, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
    main()
    logger.info('脚本 %s 运行完成, 时间：%s ' %(thisScript.name, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
    # fmt: on
