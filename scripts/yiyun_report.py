#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成易云表格格式的日报（可直接复制粘贴）
用法: python3 yiyun_report.py
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from worklog_expander import WorkLogManager
from datetime import datetime

def generate_yiyun_format():
    """生成易云表格可直接粘贴的格式"""
    manager = WorkLogManager()
    today = datetime.now().strftime('%Y-%m-%d')
    
    entries = manager.logs.get(today, [])
    
    if not entries:
        return "还没有记录今天的工作内容"
    
    lines = []
    lines.append("=" * 50)
    lines.append(f"📋 {today} 工作日志 - 易云表格格式")
    lines.append("=" * 50)
    lines.append("")
    lines.append("【复制方式】")
    lines.append("→ 选中下面每个工作项的内容")
    lines.append("→ 复制后粘贴到易云表格对应行")
    lines.append("")
    
    for i, entry in enumerate(entries, 1):
        lines.append("-" * 40)
        lines.append(f"📌 第 {i} 项工作：")
        lines.append("")
        lines.append("【工作要点】（粘贴到'工作要点'列）：")
        lines.append(entry['work_point'])
        lines.append("")
        lines.append("【取得的成果/进展】（粘贴到'成果'列）：")
        lines.append(entry['achievement'])
        lines.append("")
        lines.append(f"【工作时长】（粘贴到'时长'列）：{entry['duration']}")
        lines.append("")
        lines.append("【完成情况】（粘贴到'完成情况'列）：已完成")
        lines.append("")
    
    lines.append("=" * 50)
    lines.append(f"📊 今日总计：{len(entries)}项工作")
    total_hours = sum(e['duration'] for e in entries)
    lines.append(f"⏱️ 总时长：{total_hours}小时")
    lines.append("=" * 50)
    
    return "\n".join(lines)

def generate_compact_format():
    """生成紧凑格式（适合飞书查看）"""
    manager = WorkLogManager()
    today = datetime.now().strftime('%Y-%m-%d')
    
    entries = manager.logs.get(today, [])
    
    if not entries:
        return "还没有记录今天的工作内容"
    
    lines = [f"📅 {today} 工作日志", ""]
    
    for i, entry in enumerate(entries, 1):
        lines.append(f"━━━━━━━━━━━━━━━━━━━━━━")
        lines.append(f"【{i}】{entry['work_point']}")
        lines.append("")
        # 成果按行显示
        for line in entry['achievement'].split('\n'):
            lines.append(f"  {line}")
        lines.append("")
        lines.append(f"⏱️ {entry['duration']}小时 | ✅ 已完成")
        lines.append("")
    
    total_hours = sum(e['duration'] for e in entries)
    lines.append(f"📊 共{len(entries)}项，{total_hours}小时")
    
    return "\n".join(lines)

def main():
    print(generate_yiyun_format())

if __name__ == '__main__':
    main()
