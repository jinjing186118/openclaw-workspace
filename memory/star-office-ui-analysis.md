# Star Office UI 技术分析与部署报告

**日期**: 2026-03-01  
**状态**: ✅ 已部署运行

---

## 一、项目概览

Star-Office-UI 是一个像素风多Agent协作办公可视化面板，通过游戏化界面展示多个AI Agent的实时工作状态。

- **GitHub**: https://github.com/ringhyacinth/Star-Office-UI
- **协议**: MIT（代码），非商用（美术资产）

## 二、技术架构

### 后端 (Flask)
- **语言**: Python 3 + Flask 3.0.2
- **端口**: 18791
- **存储**: 纯文件JSON（state.json / agents-state.json / join-keys.json），无数据库
- **并发控制**: threading.Lock 保护 join 操作
- **自动离线**: 5分钟无推送自动标记offline，状态TTL 300秒自动回idle

### 核心API
| 端点 | 方法 | 功能 |
|------|------|------|
| `/agents` | GET | 获取所有agent状态 |
| `/join-agent` | POST | 注册新agent（需joinKey） |
| `/agent-push` | POST | 推送agent状态更新 |
| `/leave-agent` | POST | agent离开 |
| `/yesterday-memo` | GET | 获取昨日小日记 |
| `/health` | GET | 健康检查 |
| `/set_state` | POST | 设置主状态 |

### 前端 (Phaser 3)
- **引擎**: Phaser 3 游戏引擎
- **渲染**: 像素风办公室场景
- **区域**: breakroom(休息区)、writing(工作区)、error(错误区)
- **特性**: 精灵动画、对话气泡、移动端自适应、Demo模式

### Agent状态模型
6种状态 → 3个区域映射：
- `idle` → breakroom（休息区）
- `writing` / `researching` / `executing` / `syncing` → writing（工作区）
- `error` → error（错误区）

## 三、部署情况

### 已完成
- ✅ 代码克隆到 `/root/Star-Office-UI/`
- ✅ Flask依赖安装
- ✅ systemd服务 `star-office.service`（开机自启）
- ✅ nginx反代 18793 → 18791
- ✅ 7个bot全部注册并approved

### 端口分配
| 端口 | 服务 | 备注 |
|------|------|------|
| 18791 | Flask直连 | 内网API调用 |
| 18792 | OpenClaw Gateway | 已占用 |
| 18793 | Nginx反代 | 公网访问入口 |

### 7个Bot对接
| Agent | agentId | joinKey | 状态 |
|-------|---------|---------|------|
| 大主管 | agent_..._r59k | ocj_main | ✅ approved |
| 开发助手 | agent_..._ow8c | ocj_dev | ✅ approved |
| 材料撰写 | agent_..._wtty | ocj_content | ✅ approved |
| 热点搜集 | agent_..._svl6 | ocj_ops | ✅ approved |
| 视频分析 | agent_..._ttwl | ocj_vedio | ✅ approved |
| 公众号IP | agent_..._8j4x | ocj_brand | ✅ approved |
| 需求推广 | agent_..._sw8q | ocj_requirements | ✅ approved |

### 状态推送脚本
```bash
/root/Star-Office-UI/push-status.sh <agent> <state> [detail]
# 例: ./push-status.sh dev writing "正在写代码"
```

## 四、待办

1. **腾讯云安全组放行18793端口** → 金主人手动操作
2. **OpenClaw HEARTBEAT集成** → 让每个agent的heartbeat自动推送状态到Star Office
3. **去掉默认的Star和NPC1** → 修改DEFAULT_AGENTS只保留我们的7个bot
4. **自定义精灵** → 为7个bot设计专属像素角色（可选）
5. **"昨日小日记"对接** → MEMORY_DIR指向OpenClaw的memory目录

## 五、可行性评估

| 维度 | 评分 | 说明 |
|------|------|------|
| 技术复杂度 | ⭐⭐ 低 | 纯Flask+JSON文件，一个人完全能维护 |
| 部署难度 | ⭐ 极低 | pip install flask + systemd，完事 |
| 与OpenClaw集成 | ⭐⭐⭐ 中 | 需要写推送脚本/heartbeat hook |
| 视觉效果 | ⭐⭐⭐⭐ 好 | 像素风格有趣，比纯文本状态面板强多了 |
| 生产就绪度 | ⭐⭐ 低 | 文件存储、无认证、无HTTPS，适合内部用 |
| 可扩展性 | ⭐⭐⭐ 中 | API设计清晰，加功能比较容易 |

**结论**: 适合作为团队内部可视化面板，开机自启+nginx反代已搞定。金主人放行端口后即可公网访问。
