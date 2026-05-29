#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   aoshu_updated.py
@Time    :   2026/05/29 21:50:00
@Author  :   Ferret@NJTech
@Desc    :   二年级应用题生成器（填空版）
'''

from datetime import datetime
import logging
import random
import pathlib

START = datetime.now()
thisScript = pathlib.Path(__file__)
logLevel = logging.INFO
logFileName = f"{thisScript.stem}_{START.strftime('%Y%m%d-%H%M%S')}.log"
logFile = thisScript.with_name(logFileName)

logging.basicConfig(
    level=logLevel,
    format='%(message)s',
    handlers=[logging.FileHandler(logFile, mode='w', encoding='utf-8'), logging.StreamHandler()],
    datefmt='%Y-%m-%d %H:%M:%S'
)

logger = logging.getLogger(__name__)

def generate_he_bei_problems(num_problems=5):
    templates = [
        {
            "type": "学校班级/人数",
            "text": "某学校{group1}和{group2}共有 {total} 人，其中{group1}的人数是{group2}的 {times} 倍。{group1}有_______人，{group2}有_______人。",
            "g1": ["男生", "科技组", "合唱队"],
            "g2": ["女生", "美术组", "舞蹈队"],
            "unit": "人"
        },
        {
            "type": "农场/动物数量",
            "text": "养鸡场里{group1}和{group2}共 {total} 只，其中{group1}的只数是{group2}的 {times} 倍。{group1}有_______只，{group2}有_______只。",
            "g1": ["母鸡", "公鸡"],
            "g2": ["公鸡", "小鸡"],
            "unit": "只"
        },
        {
            "type": "水果/物品重量",
            "text": "水果店运来{group1}和{group2}共 {total} 千克，运来的{group1}重量是{group2}的 {times} 倍。{group1}有_______千克，{group2}有_______千克。",
            "g1": ["苹果", "西瓜", "梨"],
            "g2": ["香蕉", "桔子", "葡萄"],
            "unit": "千克"
        }
    ]
    
    probs, ans = [], []
    for i in range(1, num_problems + 1):
        tpl = random.choice(templates)
        val_small = random.randint(10, 50)
        times = random.randint(2, 6)
        val_big = val_small * times
        total = val_small + val_big
        
        g1_word = random.choice(tpl["g1"])
        g2_word = random.choice(tpl["g2"])
        while g1_word == g2_word:
            g2_word = random.choice(tpl["g2"])
            
        prob_text = f"({i}) " + tpl["text"].format(group1=g1_word, group2=g2_word, total=total, times=times)
        # 修正：确保答案带有物理量单位
        ans_text = f"({i}) {g1_word}：{val_big} {tpl['unit']}；{g2_word}：{val_small} {tpl['unit']}。"
        
        probs.append(prob_text)
        ans.append(ans_text)
    return probs, ans

def generate_ying_kui_problems(num_problems=5, start_index=1):
    templates = [
        {
            "intro": "老师把一袋{item}分给小朋友们。",
            "plan1": "如果每人分 {plan1_val} {unit}，则多了 {diff1} {unit}；",
            "plan2": "如果每人分 {plan2_val} {unit}，则少了 {diff2} {unit}。",
            "question": "一共有多少个小朋友？这袋{item}有多少{unit}？\n答：小朋友有_______人，{item}有_______{unit}。"
        }
    ]
    items_pool = ["糖果", "苹果", "铅笔"]
    units_pool = {"糖果": "粒", "苹果": "个", "铅笔": "支"}
    
    probs, ans = [], []
    for i in range(start_index, start_index + num_problems):
        tpl = random.choice(templates)
        item = random.choice(items_pool)
        unit = units_pool[item]
        
        base_count = random.randint(10, 25)
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
        ans_text = f"({i}) 小朋友：{base_count} 人；{item}：{total_amount} {unit}。"
        
        probs.append(prob_text)
        ans.append(ans_text)
    return probs, ans

if __name__ == '__main__':
    logger.info("=" * 20 + " 💥 二年级数学应用题练习 💥 " + "=" * 20)
    
    # 生成题目
    hb_probs, hb_ans = generate_he_bei_problems(3)
    yk_probs, yk_ans = generate_ying_kui_problems(3, start_index=4)
    
    # 输出题干
    logger.info("\n[ 一、 和倍问题 ]")
    for p in hb_probs:
        logger.info(p + "\n")
        
    logger.info("\n[ 二、 盈亏问题 ]")
    for p in yk_probs:
        logger.info(p + "\n")
    
    # 集中输出答案
    logger.info("\n" + "=" * 20 + " 💡 参考答案 💡 " + "=" * 20)
    logger.info("\n[ 和倍问题答案 ]")
    for a in hb_ans:
        logger.info(a)
        
    logger.info("\n[ 盈亏问题答案 ]")
    for a in yk_ans:
        logger.info(a)
    
    logger.info(f"\n生成完成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")