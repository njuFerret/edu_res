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
import random
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


def generate_he_bei_problems(num_problems=5):
    """
    批量生成和倍问题
    """
    templates = [
        {
            "type": "学校班级/人数",
            "text": "某学校{group1}和{group2}共有 {total} 人，其中{group1}的人数是{group2}的 {times} 倍。{group1}和{group2}各有多少人？",
            "g1": ["男生", "科技组", "合唱队"],
            "g2": ["女生", "美术组", "舞蹈队"]
        },
        {
            "type": "农场/动物数量",
            "text": "养鸡场里{group1}和{group2}共 {total} 只，其中{group1}的只数是{group2}的 {times} 倍。{group1}和{group2}各有多少只？",
            "g1": ["母鸡", "公鸡"],
            "g2": ["公鸡", "小鸡"]
        },
        {
            "type": "水果/物品重量",
            "text": "水果店运来{group1}和{group2}共 {total} 千克，运来的{group1}重量是{group2}的 {times} 倍。{group1}和{group2}各运来多少千克？",
            "g1": ["苹果", "西瓜", "梨"],
            "g2": ["香蕉", "桔子", "葡萄"]
        }
    ]
    
    generated_list = []
    
    for i in range(1, num_problems + 1):
        tpl = random.choice(templates)
        
        # 1. 先设定标准的 1倍量（小数），保证答案是整数
        val_small = random.randint(10, 50)
        # 2. 设定倍数
        times = random.randint(2, 6)
        # 3. 计算大数和总和
        val_big = val_small * times
        total = val_small + val_big
        
        # 随机选取词汇
        g1_word = random.choice(tpl["g1"])
        g2_word = random.choice(tpl["g2"])
        while g1_word == g2_word: # 避免词汇重复
            g2_word = random.choice(tpl["g2"])
            
        # 填充题目
        prob_text = f"({i}) " + tpl["text"].format(group1=g1_word, group2=g2_word, total=total, times=times)
        ans_text = f"答案：{g2_word}（1倍量）有 {val_small}；{g1_word}（{times}倍量）有 {val_big}。"
        
        generated_list.append((prob_text, ans_text))
        
    return generated_list


def generate_ying_kui_problems(num_problems=5):
    """
    批量生成盈亏问题（保留上一版的核心逻辑）
    """
    templates = [
        {
            "intro": "老师把一袋{item}分给小朋友们。",
            "plan1": "如果每人分 {plan1_val} {unit}，则多了 {diff1} {unit}；",
            "plan2": "如果每人分 {plan2_val} {unit}，则少了 {diff2} {unit}。",
            "question": "一共有多少个小朋友？这袋{item}有多少{unit}？"
        }
    ]
    items_pool = ["糖果", "苹果", "铅笔"]
    units_pool = {"糖果": "粒", "苹果": "个", "铅笔": "支"}
    
    generated_list = []
    for i in range(1, num_problems + 1):
        tpl = random.choice(templates)
        item = random.choice(items_pool)
        unit = units_pool[item]
        
        base_count = random.randint(10, 25) # 总人数
        plan1_val = random.randint(5, 10)
        step = random.randint(1, 3)
        plan2_val = plan1_val + step
        diff1 = random.randint(2, 8)
        
        total_amount = base_count * plan1_val + diff1
        diff2 = base_count * plan2_val - total_amount
        
        prob_text = f"({i}) " + tpl["intro"].format(item=item) + \
                    tpl["plan1"].format(plan1_val=plan1_val, unit=unit, diff1=diff1) + \
                    tpl["plan2"].format(plan2_val=plan2_val, unit=unit, diff2=diff2) + \
                    tpl["question"].format(item=item, unit=unit)
        ans_text = f"答案：小朋友有 {base_count} 人，{item}有 {total_amount} {unit}。"
        
        generated_list.append((prob_text, ans_text))
    return generated_list


# --- 主程序：组合输出两种题型 ---
if __name__ == '__main__':
    # fmt: off
    logger.info('脚本 %s 开始运行, 时间：%s ' %(thisScript.name, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
    logger.info("=" * 25 + " 💥 智能数学题库生成器 💥 " + "=" * 25)
    
    # 1. 生成 3 道和倍问题
    logger.info("\n一、 【和倍问题应用题】")
    he_bei_probs = generate_he_bei_problems(3)
    for p, a in he_bei_probs:
        logger.info(p)
        logger.info(a)
        logger.info("-" * 60)
        
    # 2. 生成 3 道盈亏问题
    logger.info("\n二、 【盈亏问题应用题】")
    ying_kui_probs = generate_ying_kui_problems(3)
    for p, a in ying_kui_probs:
        logger.info(p)
        logger.info(a)
        logger.info("-" * 60)
    logger.info('脚本 %s 运行完成, 时间：%s ' %(thisScript.name, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
    # fmt: on
