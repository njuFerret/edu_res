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

def generate_he_bei_problems(num_problems=5, start_index=1):
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
    for i in range(start_index, num_problems + 1):
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


def generate_implicit_he_bei_problems(num_problems=6, start_index=1):
    """
    更新后的函数：生成隐含和倍关系的应用题
    包含 6 种完全不同的经典题干类型，严格保证生成题目不重样、数据均有正整数解。
    """
    probs, ans = [], []
    # 6 种完全不同的隐含和倍变型
    sub_types = [
        "remove_zero",       # 1. 去掉末尾0 (数位变型)
        "three_objects",     # 2. 三种对象错杂关联 (复合和差)
        "four_operations",   # 3. 加减乘除四数相等 (基准量变型)
        "move_shao",         # 4. 移多补少 (变动平衡)
        "age_problem",       # 5. 年龄问题 (同步增减)
        "saw_wood"           # 6. 锯木头问题 (段数与次数)
    ]
    
    for idx, i in enumerate(range(start_index, start_index + num_problems)):
        current_type = sub_types[idx % len(sub_types)]
        
        if current_type == "remove_zero":
            # --- 类型 1: 去掉末尾的0（隐含10倍关系） ---
            val_small = random.randint(11, 89)
            val_big = val_small * 10
            total = val_small + val_big
            
            prob_text = f"({i}) 两数之和是 {total}，其中一个数的最后一位数字是 0。如果把 0 去掉，就与另一个数相同。这两个数分别是_______和_______。"
            ans_text = f"({i}) 较大数：{val_big}；较小数：{val_small}。"
            
        elif current_type == "three_objects":
            # --- 类型 2: 三种对象错杂关联（和差与倍数复合） ---
            x = random.randint(5, 20)      
            diff = random.randint(3, 8)     
            story = x + diff
            tech = story * 2
            total = x + story + tech
            
            prob_text = f"({i}) 学校买来 {total} 本书，其中科技书是故事书的 2 倍，故事书比文艺书多 {diff} 本。这三种书各有：科技书_______本，故事书_______本，文艺书_______本。"
            ans_text = f"({i}) 科技书：{tech} 本；故事书：{story} 本；文艺书：{x} 本。"
            
        elif current_type == "four_operations":
            # --- 类型 3: 加减乘除后四数相等（综合演变） ---
            multiple = 2
            delta = random.randint(1, 5)
            k = random.randint(3, 15) * 2 
            
            A = k - delta
            B = k + delta
            C = k // multiple
            D = k * multiple
            total = A + B + C + D
            
            prob_text = f"({i}) 甲、乙、丙、丁四个人一共做了 {total} 个零件。如果把甲做的个数加上 {delta}，乙做的个数减去 {delta}，丙做的个数乘以 {multiple}，丁做的个数除以 {multiple}，四个人做的零件个数正好相等。问四个人各做了多少个零件？\n答：甲_______个，乙_______个，丙_______个，丁_______个。"
            ans_text = f"({i}) 甲：{A} 个；乙：{B} 个；丙：{C} 个；丁：{D} 个。"

        elif current_type == "move_shao":
            # --- 类型 4: 移多补少（隐含“移动后变为几倍”的关系） ---
            while True:
                after_small = random.randint(5, 15)  # 移动后较少者的数量
                times = random.randint(2, 4)         # 移动后的倍数
                total = after_small * (times + 1)   # 总数保持不变
                move_num = random.randint(2, 6)      # 移动的数量
                
                brother_orig = (after_small * times) + move_num  # 倒推原本较大者
                younger_orig = after_small - move_num            # 倒推原本较小者
                if younger_orig > 0:  # 确保原本数量大于0，合法则跳出
                    break
                    
            prob_text = f"({i}) 哥哥和弟弟一共有 {total} 支铅笔。如果哥哥给弟弟 {move_num} 支铅笔，那么哥哥的铅笔支数恰好是弟弟的 {times} 倍。哥哥原本有_______支铅笔，弟弟原本有_______支铅笔。"
            ans_text = f"({i}) 哥哥原本：{brother_orig} 支；弟弟原本：{younger_orig} 支。"

        elif current_type == "age_problem":
            # --- 类型 5: 年龄问题（隐含“年龄差不变”与时间平移） ---
            past_small = random.randint(4, 12)       # 几年前女儿的年龄
            times = random.randint(3, 5)             # 几年前的倍数
            past_total = past_small * (times + 1)    # 几年前的年龄和
            years = random.randint(2, 5)             # 设定是几年前
            
            total = past_total + (years * 2)         # 今年的年龄和
            daughter_now = past_small + years        # 女儿今年年龄
            father_now = (past_small * times) + years # 爸爸今年年龄
            
            prob_text = f"({i}) 爸爸和女儿今年的年龄之和是 {total} 岁。{years} 年前，爸爸的年龄恰好是女儿的 {times} 倍。爸爸今年_______岁，女儿今年_______岁。"
            ans_text = f"({i}) 爸爸今年：{father_now} 岁；女儿今年：{daughter_now} 岁。"

        elif current_type == "saw_wood":
            # --- 类型 6: 锯木头问题（隐含“段数与次数”的植树问题变型） ---
            time_per_cut = random.randint(2, 4)      # 每锯一次需要的分钟数
            segment2 = random.randint(3, 4)          # 较少的那次锯成几段
            cut2 = segment2 - 1                      # 实际锯的次数
            time2 = cut2 * time_per_cut              # 锯少段消耗的时间
            
            times = random.randint(2, 3)             # 次数/时间的倍数关系
            cut1 = cut2 * times                      # 较多的那次实际锯的次数
            segment1 = cut1 + 1                      # 对应的段数
            time1 = cut1 * time_per_cut              # 锯多段消耗的时间
            total_time = time1 + time2               # 两次总时间
            
            prob_text = f"({i}) 一根粗细均匀的木头。木匠师傅把它锯成 {segment1} 段所用的时间，是把它锯成 {segment2} 段所用时间的 {times} 倍。已知这两次锯木头一共用了 {total_time} 分钟。锯成 {segment1} 段用了_______分钟，锯成 {segment2} 段用了_______分钟。"
            ans_text = f"({i}) 锯成 {segment1} 段：{time1} 分钟；锯成 {segment2} 段：{time2} 分钟。"

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
    logger.info("=" * 20 + " 💥 二年级数学应用题练习（自动索引版） 💥 " + "=" * 20)
    
    # 1. 定义每种题型的数量
    num_hb = 3   # 基础和倍问题数量
    num_ihb = 6  # 隐含和倍问题数量
    num_yk = 3   # 盈亏问题数量
    
    # 2. 初始化起始题号计数器
    current_index = 1
    
    # 3. 自动索引生成：基础和倍问题 (序号: 1 ~ 3)
    hb_probs, hb_ans = generate_he_bei_problems(num_problems=num_hb, start_index=current_index)
    current_index += num_hb  # 计数器自动累加 3，变为 4
    
    # 4. 自动索引生成：隐含和倍问题 (序号: 4 ~ 9)
    ihb_probs, ihb_ans = generate_implicit_he_bei_problems(num_problems=num_ihb, start_index=current_index)
    current_index += num_ihb # 计数器自动累加 6，变为 10
    
    # 5. 自动索引生成：盈亏问题     (序号: 10 ~ 12)
    yk_probs, yk_ans = generate_ying_kui_problems(num_problems=num_yk, start_index=current_index)
    
    # --- 输出题干 ---
    logger.info("\n[ 一、 基础和倍问题 ]")
    for p in hb_probs:
        logger.info(p + "\n")
        
    logger.info("\n[ 二、 隐含和倍问题 ]")
    for p in ihb_probs:
        logger.info(p + "\n")
        
    logger.info("\n[ 三、 盈亏问题 ]")
    for p in yk_probs:
        logger.info(p + "\n")
    
    # --- 集中输出答案 ---
    logger.info("\n" + "=" * 20 + " 💡 参考答案 💡 " + "=" * 20)
    logger.info("\n[ 基础和倍问题答案 ]")
    for a in hb_ans:
        logger.info(a)
        
    logger.info("\n[ 隐含和倍问题答案 ]")
    for a in ihb_ans:
        logger.info(a)
        
    logger.info("\n[ 盈亏问题答案 ]")
    for a in yk_ans:
        logger.info(a)
    
    logger.info(f"\n生成完成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")