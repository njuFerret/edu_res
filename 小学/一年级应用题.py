#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   aoshu_1.py
@Time    :   2025/06/17 09:36:30
@Author  :   Ferret@NJTech
@Version :   1.0
@Contact :   Ferret@NJTech
@License :   (C)Copyright 2025, Ferret@NJTech
@Desc    :   补充描述
'''

from datetime import datetime
import logging
import numpy as np
import json
import pathlib

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


def candies(prompt, ques_type) -> dict:

    key = f"type_{ques_type}"
    questions = {key: {'data': [], 'count': 0}}
    nKid = np.random.randint(3, 6, 50)
    # s = prompt[0]
    for kid in nKid:
        s = prompt[0].format(kid)
        ammounts = np.random.randint(-10, 10, kid - 1)
        # base = 0
        unit = np.random.randint(5, 15, 1)
        for idx, ammount in enumerate(ammounts):
            # base -= ammounts[: idx + 1].sum()
            unit = np.append(unit, unit[idx] - ammount)
            if ammount > 0:
                s += f"第{idx+1}个小朋友比第{idx+2}个小朋友多{prompt[1]}{ammount}{prompt[2]}, "
            elif ammount == 0:
                s += f"第{idx+1}个小朋友和第{idx+2}个小朋友一样多, "
            else:
                s += f"第{idx+1}个小朋友比第{idx+2}个小朋友少{prompt[1]}{-ammount}{prompt[2]}, "

        if (unit < 0).any():
            # print(f"------------------尼玛--------------------------: {unit}")
            continue
        s += prompt[3].format(unit.sum())

        questions[key]['data'].append({'q': s, 'a': unit.tolist()})
    questions[key]['count'] = len(questions[key]['data'])
    return questions


def testGenerate(all_ques: dict, count=10):
    question = {}

    # 获取所有类型题目的数量
    counts = [v['count'] for v in all_ques.values()]
    # 选取数量需要小于所有题型最少的数量
    valid_count = min(counts)
    if count > valid_count:
        count = valid_count

    # 随机选取count个题目的索引
    selects = np.array([np.random.choice(c, count, replace=False) for c in counts])

    print(selects)

    # 从数据中获取提取满足索引的题目，此时为一维数组，shape 为: (len(all_ques) x count,)
    questions = np.array([v['data'][c] for idx, v in enumerate(all_ques.values()) for c in selects[idx]])
    # 变换数组形状，shape 为: (3 x count,)
    questions = questions.reshape(len(all_ques), -1).T  # shape: (count, 3)

    # print(questions)

    qq = []
    aa = []
    for idx, question in enumerate(questions):
        qq.extend([f'Q{idx*3+j+1:02d}. ' + q['q'] for j, q in enumerate(question)])
        aa.extend([f'Q{idx*3+j+1:02d}. ' + str(q['a']) for j, q in enumerate(question)])

    logger.info("\n".join(qq))
    logger.info("----------------" * 4)
    logger.info("\n".join(aa))

    # data = zip(selects, v['data']) for idx, v in enumerate(all_ques.values())

    # for idx, select in zip(selects,questions):

    # print(list(zip(all_ques[])))

    # for idx in range(len(all_ques)):
    #     print(min(all_ques[f'type_{idx}']['count']))
    # for item in all_ques.values():
    #     if valid_count > item['count']:
    #         valid_count = item['count']

    #     selects = np.random.choice(item['count'], valid_count, replace=False).tolist()
    #     data = [item['data'][i] for i in selects]
    #     # print(item)
    #     for sub_inx, select in enumerate(selects):
    #         s = f"Q{idx*3+sub_inx+1:02d}. " + data[select]['q']
    #         question[s] = data[select]['a']

    # logger.info(json.dumps(question, indent=2, ensure_ascii=False))


def main():

    prompts = [
        ['有{}个小朋友分糖果, ', '分', '个', '一共有{}个糖果, 则每个小朋友分几个?'],
        ['有{}个小朋友买文具, ', '花', '元', '一共花了{}元, 则每个小朋友花了多少元?'],
        ['有{}个小朋友做手工, ', '做', '个', '一共做了{}个, 则每个小朋友做了多少个?'],
    ]
    questions = {}
    for idx, prompt in enumerate(prompts):
        questions.update(candies(prompt=prompt, ques_type=idx))

    testGenerate(questions)


if __name__ == '__main__':
    # fmt: off
    logger.info('脚本 %s 开始运行, 时间：%s ' %(thisScript.name, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
    main()
    logger.info('脚本 %s 运行完成, 时间：%s ' %(thisScript.name, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
    # fmt: on
