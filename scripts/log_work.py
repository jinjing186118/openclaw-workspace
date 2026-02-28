#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
工作日志记录命令
用法: python3 log_work.py "上午跟研发开需求评审会，2.5小时"
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from worklog_expander import WorkLogManager

def main():
    if len(sys.argv) < 2:
        print("用法: python3 log_work.py \"工作描述\"")
        print("示例: python3 log_work.py \"上午跟研发开需求评审会，2.5小时\"")
        print("      python3 log_work.py \"调研OpenClaw工具，完成定时任务配置\"")
        sys.exit(1)
    
    brief = sys.argv[1]
    manager = WorkLogManager()
    
    from datetime import datetime
    today = datetime.now().strftime('%Y-%m-%d')
    
    entry = manager.add_entry(today, brief)
    
    print("✅ 已记录工作：")
    print(f"工作要点：{entry['work_point']}")
    print(f"建议时长：{entry['duration']}小时")
    print("\n成果扩写预览（部分）：")
    preview = entry['achievement'].split('\n')[0][:50] + "..."
    print(f"  {preview}")

if __name__ == '__main__':
    main()
