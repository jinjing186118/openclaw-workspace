# OpenClaw Workspace

金金的 OpenClaw 统一工作空间

## 📁 目录结构

| 文件/目录 | 说明 |
|----------|------|
| `SOUL.md` | Bot 灵魂定义 |
| `AGENTS.md` | 团队 Bot 定义 |
| `IDENTITY.md` | 身份设定 |
| `USER.md` | 用户偏好 |
| `MEMORY.md` | 长期记忆 |
| `HEARTBEAT.md` | 定时任务 |
| `memory/` | 按日期记忆 |
| `skills/` | 自定义技能 |
| `scripts/` | 自定义脚本 |

## 🚀 部署

```bash
# 拉取最新配置
git pull origin main

# 重启 OpenClaw
openclaw gateway restart
```

## 📝 更新流程

1. 在 Mac/iMac 上修改文件
2. `git commit -m "描述"`
3. `git push origin main`
4. 腾讯云自动/手动拉取重启

---
_多端统一，配置即代码_
