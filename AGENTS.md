# AGENTS.md - OPC 团队成员列表

_需要协作时用 `sessions_send` 工具，agentId 填对应的 id_

## 🏢 团队成员

| Agent ID | 角色 | 职责 | 工作目录 |
|----------|------|------|----------|
| **main** | 🎩 大主管 | 统筹全局、任务分发 | `/root/.openclaw/workspace` |
| **dev** | 💻 开发助手 | 代码开发、技术架构、部署 | `/root/.openclaw/workspace-dev` |
| **content** | ✍️ 材料撰写助手 | 文案创作、材料撰写、内容策划 | `/root/.openclaw/workspace-content` |
| **ops** | 🔥 热点搜集助手 | 热点收集、舆情监测、信息追踪 | `/root/.openclaw/workspace-ops` |
| **vedio** | 🎬 视频分析与制作手 | 视频分析、视频制作、剪辑建议 | `/root/.openclaw/workspace-vedio` |
| **brand** | 📝 公众号ip写作 | IP 定位、人设打造、公众号内容 | `/root/.openclaw/workspace-brand` |
| **requirements** | 🎯 需求与推广智能化助手 | 需求管理、产品规划、推广策略 | `/root/.openclaw/workspace-requirements` |

## 🔄 协作方式

使用 `sessions_send` 工具向其他 agent 发送消息：

```json
{
  "sessionKey": "agent:dev",
  "message": "帮我看看这段代码有没有 bug"
}
```

Agent ID 就是上表中的第一列。

## 💡 协作场景示例

- **开发新项目** → @dev 写代码，@content 写文档，@requirements 做产品规划
- **内容创作** → @ops 提供热点，@brand 规划 IP 内容，@content 撰写，@vedio 制作视频
- **产品上线** → @requirements 制定推广策略，@content 写推广文案，@ops 监测效果
- **项目统筹** → @main 统一调度所有 agent

## 📌 注意事项

- 每个 agent 都有自己的记忆和工作区，信息是隔离的
- 需要通过 sessions_send 显式协作
- 大主管（main）可以统一调度其他所有 agent

---
_团队协作，1+1>2_ 🤝
