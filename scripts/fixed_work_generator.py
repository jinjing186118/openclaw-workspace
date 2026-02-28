#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
每日固定工作自动生成器
用于生成每天必做的重复性工作日志
"""

import random
import json
import os
import sys
from datetime import datetime

# 固定工作配置
FIXED_WORK_CONFIG = {
    "work_point": "需求扎口与流转",
    "duration_range": [2.0, 3.0],  # 时长范围 2-3小时
    "achievement_templates": [
        {
            "lines": [
                "1、完成智研平台 {num1} 条需求扎口与流转",
                "2、完成 OA 内 {num2} 条新增需求的规范性审核与流转",
                "3、解答 {num3} 名研发中心同事的需求流转问题"
            ],
            "num_ranges": {
                "num1": [3, 8],      # 智研平台需求数
                "num2": [2, 6],      # OA需求数
                "num3": [2, 5]       # 解答同事数
            }
        },
        {
            "lines": [
                "1、完成智研平台 {num1} 个需求的扎口评估与流程推进",
                "2、审核并流转 OA 系统 {num2} 个新增需求",
                "3、响应并解决 {num3} 位研发同事的需求流转咨询"
            ],
            "num_ranges": {
                "num1": [4, 9],
                "num2": [3, 7],
                "num3": [3, 6]
            }
        },
        {
            "lines": [
                "1、推进智研平台 {num1} 项需求的扎口与会签流程",
                "2、完成 OA 内 {num2} 个需求条目的规范审核与分发",
                "3、支持 {num3} 名研发中心同事完成需求提报与流转"
            ],
            "num_ranges": {
                "num1": [2, 7],
                "num2": [2, 5],
                "num3": [2, 4]
            }
        },
        {
            "lines": [
                "1、处理智研平台 {num1} 条需求的扎口审批与状态更新",
                "2、审核 OA 内 {num2} 个新增需求并推进流转",
                "3、解答 {num3} 位研发同事关于需求流转的疑问"
            ],
            "num_ranges": {
                "num1": [3, 7],
                "num2": [2, 6],
                "num3": [2, 5]
            }
        }
    ]
}

class FixedWorkGenerator:
    """固定工作生成器"""
    
    @classmethod
    def generate_daily_fixed_work(cls) -> dict:
        """生成今天的固定工作"""
        config = FIXED_WORK_CONFIG
        
        # 随机选择一套模板
        template = random.choice(config["achievement_templates"])
        
        # 生成随机数字
        numbers = {}
        for key, range_vals in template["num_ranges"].items():
            numbers[key] = random.randint(range_vals[0], range_vals[1])
        
        # 生成成果文本
        achievement_lines = []
        for line_template in template["lines"]:
            achievement_lines.append(line_template.format(**numbers))
        
        # 随机时长（2-3小时，可以有0.5的小数）
        duration = round(random.uniform(
            config["duration_range"][0], 
            config["duration_range"][1]
        ) * 2) / 2  # 确保是0.5的倍数
        
        return {
            "work_point": config["work_point"],
            "achievement": "\n".join(achievement_lines),
            "duration": duration,
            "brief": "每日固定工作：需求扎口与流转"
        }
    
    @classmethod
    def add_to_today_logs(cls):
        """将固定工作添加到今天的日志"""
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        from worklog_expander import WorkLogManager
        
        manager = WorkLogManager()
        today = datetime.now().strftime('%Y-%m-%d')
        
        # 生成固定工作
        fixed_work = cls.generate_daily_fixed_work()
        
        # 检查今天是否已经有固定工作了
        existing = manager.logs.get(today, [])
        for entry in existing:
            if entry.get("is_fixed_work"):
                print(f"今天已经有固定工作记录了：{entry['work_point']} {entry['duration']}小时")
                return None
        
        # 添加到日志
        entry = {
            "brief": fixed_work["brief"],
            "work_point": fixed_work["work_point"],
            "achievement": fixed_work["achievement"],
            "duration": fixed_work["duration"],
            "timestamp": datetime.now().isoformat(),
            "is_fixed_work": True  # 标记为固定工作
        }
        
        if today not in manager.logs:
            manager.logs[today] = []
        
        manager.logs[today].append(entry)
        manager._save_logs()
        
        return entry


def main():
    """测试生成"""
    print("📝 生成今日固定工作\n")
    
    # 测试生成5次看随机效果
    for i in range(5):
        work = FixedWorkGenerator.generate_daily_fixed_work()
        print(f"--- 示例 {i+1} ---")
        print(f"工作要点：{work['work_point']}")
        print(f"成果：\n{work['achievement']}")
        print(f"时长：{work['duration']}小时")
        print()
    
    # 实际添加到今天的日志
    print("=" * 50)
    print("实际添加到今日日志：")
    entry = FixedWorkGenerator.add_to_today_logs()
    if entry:
        print(f"✅ 已添加：{entry['work_point']} {entry['duration']}小时")
        print(f"成果：\n{entry['achievement']}")
    

if __name__ == '__main__':
    import sys
    main()
