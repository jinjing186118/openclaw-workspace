#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
工作日志智能扩写与价值提炼系统
根据简单要点，自动生成充实、有价值的工作日志
"""

import json
import os
from datetime import datetime
from typing import List, Dict

# 工作日志存储文件
LOGS_FILE = os.path.join(os.path.dirname(__file__), '..', 'memory', 'work_logs.json')

class WorkLogExpander:
    """工作日志智能扩写器"""
    
    # 价值关键词库
    VALUE_KEYWORDS = {
        "调研": ["深度调研", "可行性分析", "技术选型", "方案对比", "形成决策依据"],
        "开发": ["功能开发", "模块搭建", "代码实现", "架构设计", "技术攻坚"],
        "会议": ["需求对齐", "方案评审", "跨部门协同", "决策制定", "风险识别"],
        "文档": ["知识沉淀", "规范制定", "流程梳理", "经验总结", "标准化建设"],
        "测试": ["质量保障", "问题发现", "风险预防", "验收标准", "上线准备"],
        "优化": ["效率提升", "体验改进", "性能优化", "成本控制", "质量提升"],
        "沟通": ["需求澄清", "进度同步", "问题协调", "资源调配", "关系维护"],
        "培训": ["能力赋能", "知识传递", "团队建设", "人才培养", "经验分享"],
    }
    
    # 成果模板
    ACHIEVEMENT_TEMPLATES = [
        "完成{subject}的{action}，明确{result}",
        "推进{subject}落地，实现{result}",
        "完成{subject}的{action}，形成{result}",
        "组织{subject}，达成{result}，为后续{future}奠定基础",
        "完成{subject}，输出{result}，助力{future}",
        "推进{subject}，解决{result}，保障{future}",
        "开展{subject}，沉淀{result}，赋能{future}",
    ]
    
    @classmethod
    def expand_achievement(cls, brief: str) -> Dict[str, str]:
        """
        根据简单描述，智能扩写工作要点和成果
        
        Args:
            brief: 用户简单描述，如 "调研 OpenClaw 工具"
            
        Returns:
            {
                "work_point": "工作要点（包装后）",
                "achievement": "取得的成果/进展（扩写后）",
                "duration": "建议时长（小时）"
            }
        """
        # 提取关键词
        keywords_found = []
        for keyword, values in cls.VALUE_KEYWORDS.items():
            if keyword in brief:
                keywords_found.extend(values)
        
        # 智能识别工作类型
        work_type = cls._detect_work_type(brief)
        
        # 生成工作要点（包装）
        work_point = cls._generate_work_point(brief, work_type)
        
        # 生成成果（扩写）
        achievement = cls._generate_achievement(brief, work_type, keywords_found)
        
        # 建议时长
        duration = cls._estimate_duration(brief, work_type)
        
        return {
            "work_point": work_point,
            "achievement": achievement,
            "duration": duration
        }
    
    @classmethod
    def _detect_work_type(cls, brief: str) -> str:
        """识别工作类型"""
        type_patterns = {
            "调研": ["调研", "研究", "考察", "了解", "学习", "试用", "测试"],
            "开发": ["开发", "编写", "搭建", "实现", " coding", "程序", "代码"],
            "会议": ["会议", "评审", "讨论", "对齐", "沟通会", "站会", "例会"],
            "文档": ["文档", "方案", "报告", "总结", "规范", "制度", "流程"],
            "优化": ["优化", "改进", "提升", "完善", "重构", "调整"],
            "协调": ["协调", "沟通", "对接", "联系", "确认", "跟进"],
        }
        
        brief_lower = brief.lower()
        for work_type, patterns in type_patterns.items():
            for pattern in patterns:
                if pattern in brief_lower:
                    return work_type
        
        return "其他"
    
    @classmethod
    def _generate_work_point(cls, brief: str, work_type: str) -> str:
        """生成包装后的工作要点"""
        point_templates = {
            "调研": "{subject}深度调研与可行性验证",
            "开发": "{subject}功能开发与模块实现",
            "会议": "{subject}需求对齐与方案评审",
            "文档": "{subject}方案设计与知识沉淀",
            "优化": "{subject}优化升级与体验提升",
            "协调": "{subject}跨部门协同与资源调配",
            "其他": "{subject}专项工作推进",
        }
        
        # 提取核心主题
        subject = cls._extract_subject(brief)
        
        template = point_templates.get(work_type, point_templates["其他"])
        return template.format(subject=subject)
    
    @classmethod
    def _generate_achievement(cls, brief: str, work_type: str, keywords: List[str]) -> str:
        """生成扩写后的成果"""
        subject = cls._extract_subject(brief)
        
        # 根据工作类型选择扩写策略
        if work_type == "调研":
            return cls._expand_research(subject, brief)
        elif work_type == "开发":
            return cls._expand_development(subject, brief)
        elif work_type == "会议":
            return cls._expand_meeting(subject, brief)
        elif work_type == "文档":
            return cls._expand_document(subject, brief)
        else:
            return cls._expand_generic(subject, brief, work_type)
    
    @classmethod
    def _expand_research(cls, subject: str, brief: str) -> str:
        """扩写调研类成果"""
        # 清理subject，去掉冗余词
        clean_subject = subject.replace('调研', '').replace('研究', '').strip('，, ')
        return f"""1. 完成{clean_subject}的深度调研，梳理核心功能模块与技术架构
2. 验证{clean_subject}在业务场景的适用性，形成可行性评估报告
3. 输出可落地的技术方案与实施路径，为后续项目决策提供依据"""
    
    @classmethod
    def _expand_development(cls, subject: str, brief: str) -> str:
        """扩写开发类成果"""
        clean_subject = subject.replace('开发', '').replace('编写', '').strip('，, ')
        return f"""1. 完成{clean_subject}核心功能开发，实现预期业务目标
2. 编写技术文档与使用说明，沉淀开发经验
3. 完成功能自测与问题修复，保障交付质量"""
    
    @classmethod
    def _expand_meeting(cls, subject: str, brief: str) -> str:
        """扩写会议类成果"""
        clean_subject = subject.replace('会议', '').replace('开', '').strip('，, ')
        return f"""1. 组织并完成{clean_subject}，对齐各方诉求与期望
2. 识别关键风险点与依赖项，制定应对策略
3. 明确下一步行动计划与责任人，推动项目落地"""
    
    @classmethod
    def _expand_document(cls, subject: str, brief: str) -> str:
        """扩写文档类成果"""
        clean_subject = subject.replace('文档', '').replace('写了', '').strip('，, ')
        return f"""1. 完成{clean_subject}方案设计，明确实施路径与验收标准
2. 梳理相关流程与规范，形成标准化操作手册
3. 完成知识沉淀与分享，提升团队整体能力"""
    
    @classmethod
    def _expand_generic(cls, subject: str, brief: str, work_type: str) -> str:
        """通用扩写"""
        return f"""1. 完成{subject}相关工作，达成阶段目标
2. 梳理问题与解决方案，形成可复用的经验
3. 为后续工作推进奠定基础，保障项目进度"""
    
    @classmethod
    def _extract_subject(cls, brief: str) -> str:
        """提取工作主题"""
        import re
        
        # 去掉时间前缀
        time_patterns = [
            r'^上午[，,、\s]*',
            r'^下午[，,、\s]*',
            r'^晚上[，,、\s]*',
            r'^今天[，,、\s]*',
            r'^刚才[，,、\s]*',
            r'^[\d]+[\.:][\d]+[，,、\s]*',
            r'^[\d]+\s*个?半小时?[，,、\s]*',
        ]
        
        subject = brief
        for pattern in time_patterns:
            subject = re.sub(pattern, '', subject)
        
        # 去掉常见的动词前缀
        prefixes = ["完成", "进行", "开展", "组织", "参加", "写了", "做了", "搞了", "弄了", "试了", "跟", "和"]
        for prefix in prefixes:
            if subject.startswith(prefix):
                subject = subject[len(prefix):].strip()
        
        # 去掉时长后缀
        subject = re.sub(r'[，,、\s]*[\d\.]+\s*个?小时?\s*$', '', subject)
        subject = re.sub(r'[，,、\s]*\d+h\s*$', '', subject, flags=re.I)
        
        # 截取合适长度
        if len(subject) > 30:
            subject = subject[:30]
        
        return subject.strip() or brief[:20]
    
    @classmethod
    def _estimate_duration(cls, brief: str, work_type: str) -> float:
        """估算工作时长"""
        # 检查是否包含时间信息
        import re
        time_patterns = [
            r'(\d+)\.?(\d*)\s*小时?',
            r'(\d+)\.?(\d*)\s*h',
            r'半?天',
            r'(\d+)\.?(\d*)\s*个?小时',
        ]
        
        for pattern in time_patterns:
            match = re.search(pattern, brief)
            if match:
                if '天' in brief:
                    return 4.0 if '半' in brief else 8.0
                try:
                    return float(match.group(1) + '.' + (match.group(2) or '0'))
                except:
                    pass
        
        # 默认时长
        default_durations = {
            "调研": 2.0,
            "开发": 3.0,
            "会议": 1.0,
            "文档": 2.0,
            "优化": 2.5,
            "协调": 1.5,
            "其他": 2.0,
        }
        return default_durations.get(work_type, 2.0)


class WorkLogManager:
    """工作日志管理器"""
    
    def __init__(self):
        self.logs = self._load_logs()
    
    def _load_logs(self) -> Dict:
        """加载历史日志"""
        if os.path.exists(LOGS_FILE):
            try:
                with open(LOGS_FILE, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                pass
        return {}
    
    def _save_logs(self):
        """保存日志"""
        os.makedirs(os.path.dirname(LOGS_FILE), exist_ok=True)
        with open(LOGS_FILE, 'w', encoding='utf-8') as f:
            json.dump(self.logs, f, ensure_ascii=False, indent=2)
    
    def add_entry(self, date: str, brief: str) -> Dict:
        """添加一条工作记录"""
        if date not in self.logs:
            self.logs[date] = []
        
        expanded = WorkLogExpander.expand_achievement(brief)
        entry = {
            "brief": brief,
            "work_point": expanded["work_point"],
            "achievement": expanded["achievement"],
            "duration": expanded["duration"],
            "timestamp": datetime.now().isoformat(),
        }
        
        self.logs[date].append(entry)
        self._save_logs()
        return entry
    
    def get_daily_report(self, date: str = None) -> str:
        """生成日报格式"""
        if date is None:
            date = datetime.now().strftime('%Y-%m-%d')
        
        entries = self.logs.get(date, [])
        if not entries:
            return None
        
        # 生成易云表格格式
        lines = []
        for i, entry in enumerate(entries, 1):
            lines.append(f"{i}. {entry['work_point']}")
            lines.append(f"   {entry['achievement'].replace(chr(10), ' ')}")
            lines.append(f"   时长：{entry['duration']}小时")
            lines.append("")
        
        return "\n".join(lines)
    
    def get_formatted_table(self, date: str = None) -> str:
        """生成完整的表格格式"""
        if date is None:
            date = datetime.now().strftime('%Y-%m-%d')
        
        entries = self.logs.get(date, [])
        if not entries:
            return None
        
        lines = [f"📅 {date} 工作日志", ""]
        
        for i, entry in enumerate(entries, 1):
            lines.append(f"【{i}】{entry['work_point']}")
            lines.append(f"成果：{entry['achievement']}")
            lines.append(f"时长：{entry['duration']}小时 | 状态：已完成")
            lines.append("")
        
        return "\n".join(lines)


def main():
    """测试"""
    manager = WorkLogManager()
    
    # 测试扩写
    test_cases = [
        "上午跟研发开需求评审会，2.5小时",
        "下午调研OpenClaw，试了定时任务",
        "写了技术方案文档",
    ]
    
    today = datetime.now().strftime('%Y-%m-%d')
    
    print("📝 工作日志智能扩写测试\n")
    for brief in test_cases:
        print(f"原始输入：{brief}")
        entry = manager.add_entry(today, brief)
        print(f"工作要点：{entry['work_point']}")
        print(f"成果扩写：{entry['achievement']}")
        print(f"建议时长：{entry['duration']}小时")
        print("-" * 50)
    
    print("\n📊 生成的日报：")
    report = manager.get_formatted_table(today)
    print(report)


if __name__ == '__main__':
    main()
