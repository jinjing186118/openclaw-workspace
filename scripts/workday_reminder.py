#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
工作日志提醒 - 智能版
包含：工作日判断 + 日报生成 + 飞书发送
"""

import requests
import json
import os
import sys
from datetime import datetime
import subprocess

# 配置文件路径
CONFIG_FILE = os.path.join(os.path.dirname(__file__), '..', 'config', 'workday_reminder.json')

def get_cn_holidays(year=None):
    """获取中国节假日数据"""
    if year is None:
        year = datetime.now().year
    
    cache_file = f"/tmp/china_holidays_{year}.json"
    if os.path.exists(cache_file):
        try:
            with open(cache_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            pass
    
    try:
        url = f"https://cdn.jsdelivr.net/gh/NateScarlet/holiday-cn@master/{year}.json"
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            try:
                with open(cache_file, 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False)
            except:
                pass
            return data
    except Exception as e:
        print(f"API 请求失败: {e}", file=sys.stderr)
    
    return None

def is_workday(date=None):
    """判断指定日期是否是中国工作日"""
    if date is None:
        date = datetime.now()
    
    date_str = date.strftime('%Y-%m-%d')
    weekday = date.weekday()
    
    holidays = get_cn_holidays(date.year)
    
    if holidays and 'days' in holidays:
        for day in holidays['days']:
            if day['date'] == date_str:
                if day['isOffDay']:
                    return False, f"节假日: {day.get('name', '未知节日')}"
                else:
                    return True, f"倒休工作日: {day.get('name', '调休')}"
    
    if weekday < 5:
        return True, "常规工作日(无节假日数据)"
    else:
        return False, "周末"

def generate_daily_report():
    """生成易云表格格式的日报"""
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from worklog_expander import WorkLogManager
    from fixed_work_generator import FixedWorkGenerator
    
    # 先自动生成今日固定工作
    fixed_entry = FixedWorkGenerator.add_to_today_logs()
    if fixed_entry:
        print(f"📝 已自动生成固定工作：{fixed_entry['work_point']} {fixed_entry['duration']}小时")
    
    manager = WorkLogManager()
    today = datetime.now().strftime('%Y-%m-%d')
    
    entries = manager.logs.get(today, [])
    
    if not entries:
        return f"""📝 工作日志提醒

今天是 {today}，该写今天的工作日志啦~

💡 你还没有记录今天的工作内容
随时跟我说今天做了什么，格式例如：
• 需求扎口与流转 2
  1、完成智研平台需求扎口与流转
  2、完成 OA 内新增需求的规范性审核与流转
  3、解答2名研发中心同事的需求流转问题

我会帮你整理成易云表格格式！"""
    
    # 生成易云表格格式
    lines = [f"📋 {today} 工作日志 - 易云表格格式", ""]
    lines.append("【复制方式】选中下面内容，复制粘贴到易云表格对应列")
    lines.append("")
    
    for i, entry in enumerate(entries, 1):
        is_fixed = "【固定】" if entry.get("is_fixed_work") else ""
        lines.append(f"━━━━━━━━━━━━━━━━━━━━━━")
        lines.append(f"📌 第 {i} 项工作：{is_fixed}")
        lines.append("")
        lines.append(f"【工作要点】→ 粘贴到'工作要点'列：")
        lines.append(entry['work_point'])
        lines.append("")
        lines.append(f"【成果】→ 粘贴到'成果'列：")
        lines.append(entry['achievement'])
        lines.append("")
        lines.append(f"【时长】→ 粘贴到'时长'列：{entry['duration']}")
        lines.append(f"【完成情况】→ 粘贴到'完成情况'列：已完成")
        lines.append("")
    
    total_hours = sum(e['duration'] for e in entries)
    lines.append(f"━━━━━━━━━━━━━━━━━━━━━━")
    lines.append(f"📊 今日总计：{len(entries)}项工作，{total_hours}小时")
    
    return "\n".join(lines)

def send_reminder(message):
    """发送飞书消息"""
    config = {}
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                config = json.load(f)
        except:
            pass
    
    target = config.get('target', 'ou_216e8e13eaf1a67e99c5e7c04245b429')
    channel = config.get('channel', 'feishu')
    
    cmd = [
        'openclaw', 'message', 'send',
        '--channel', channel,
        '--target', target,
        '--message', message
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        if result.returncode == 0:
            print(f"✅ 提醒发送成功")
            return True
        else:
            print(f"❌ 发送失败: {result.stderr}", file=sys.stderr)
            return False
    except Exception as e:
        print(f"❌ 执行失败: {e}", file=sys.stderr)
        return False

def main():
    print(f"📅 工作日志提醒检查 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    is_work, reason = is_workday()
    weekdays = ['周一','周二','周三','周四','周五','周六','周日']
    
    print(f"📊 今天是: {datetime.now().strftime('%Y-%m-%d')} {weekdays[datetime.now().weekday()]}")
    print(f"📊 工作日判断: {'是' if is_work else '否'} - {reason}")
    
    if is_work:
        print("📝 今天需要提醒，正在生成日报并发送...")
        message = generate_daily_report()
        send_reminder(message)
    else:
        print("😴 今天不需要提醒，跳过")

if __name__ == '__main__':
    main()
