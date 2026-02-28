#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成日报并发送提醒
用法: python3 daily_report.py [--send]
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from worklog_expander import WorkLogManager
from datetime import datetime
import subprocess

def generate_report(send=False):
    manager = WorkLogManager()
    today = datetime.now().strftime('%Y-%m-%d')
    
    entries = manager.logs.get(today, [])
    
    if not entries:
        message = f"📝 工作日志提醒\n\n今天是 {today}，该写今天的工作日志啦~\n\n💡 你还没有记录今天的工作内容\n随时跟我说今天做了什么，我会帮你整理成专业的日志格式！"
    else:
        # 生成易云表格格式
        lines = [f"📝 {today} 工作日志（已生成，可直接复制到易云表格）", ""]
        total_hours = 0
        
        for i, entry in enumerate(entries, 1):
            lines.append(f"【{i}】{entry['work_point']}")
            lines.append(f"成果：{entry['achievement']}")
            lines.append(f"时长：{entry['duration']}小时 | 状态：已完成")
            lines.append("")
            total_hours += entry['duration']
        
        lines.append(f"📊 今日总计：{len(entries)}项工作，{total_hours:.1f}小时")
        lines.append("")
        lines.append("💡 提示：复制以上内容到易云表格即可提交")
        
        message = "\n".join(lines)
    
    if send:
        # 发送飞书消息
        config_file = os.path.join(os.path.dirname(__file__), '..', 'config', 'workday_reminder.json')
        import json
        config = {}
        if os.path.exists(config_file):
            with open(config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)
        
        target = config.get('target', 'ou_216e8e13eaf1a67e99c5e7c04245b429')
        channel = config.get('channel', 'feishu')
        
        # 转义换行符
        message_escaped = message.replace('\n', '\\n').replace('"', '\\"')
        
        cmd = [
            'openclaw', 'message', 'send',
            '--channel', channel,
            '--target', target,
            '--message', message
        ]
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            if result.returncode == 0:
                print(f"✅ 日报提醒发送成功")
                return True
            else:
                print(f"❌ 发送失败: {result.stderr}", file=sys.stderr)
                return False
        except Exception as e:
            print(f"❌ 执行失败: {e}", file=sys.stderr)
            return False
    else:
        print(message)
        return True

def main():
    send = '--send' in sys.argv
    generate_report(send)

if __name__ == '__main__':
    main()
