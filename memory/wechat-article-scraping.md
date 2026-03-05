# 微信公众号文章抓取方法（全Bot共享）

_创建日期：2026-03-01 | 来源：ops实测验证_

## 方案：Playwright 无头浏览器渲染

### 工具依赖
- **Playwright** (Node.js) + **Chromium** 
- 已安装在 `/root/.openclaw/workspace-ops/`
- 前置：`npm install playwright` + `npx playwright install chromium`

### 一句话流程
输入微信URL → Playwright启动无头Chromium → 加载页面等待JS渲染(10s) → 提取`#js_content`正文 → 输出全文

### 任意Bot调用命令

```bash
cd /root/.openclaw/workspace-ops && node -e "
const { chromium } = require('playwright');
const URL = '这里填微信文章链接';
(async () => {
  const b = await chromium.launch({headless:true,args:['--no-sandbox','--disable-setuid-sandbox','--disable-dev-shm-usage']});
  const c = await b.newContext({
    userAgent:'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
    locale:'zh-CN',
    timezoneId:'Asia/Shanghai'
  });
  const p = await c.newPage();
  await p.addInitScript(()=>{Object.defineProperty(navigator,'webdriver',{get:()=>undefined})});
  await p.goto(URL,{waitUntil:'domcontentloaded',timeout:30000});
  await p.waitForTimeout(10000);
  const t = await p.evaluate(()=>{
    const sels = ['#js_content','.rich_media_content','#js_article','article'];
    for (const s of sels) { const e=document.querySelector(s); if(e&&e.innerText.length>100) return e.innerText; }
    return document.body.innerText;
  });
  console.log(t);
  await b.close();
})();
" 2>&1
```

### 能力边界

| ✅ 能抓 | ❌ 不能抓 |
|---------|----------|
| 普通公众号文章全文 | 付费/仅关注可见的文章 |
| 标题、作者、正文 | 文章内图片（只拿文字） |
| 历史文章（链接有效即可） | 已删除/404文章 |
| 长文（5000字+已验证） | 视频号内容 |
| 带代码块/表格的文章 | 小程序内嵌内容 |

### 注意事项
- 等待时间需8-10秒（微信JS渲染慢）
- 单次执行约15-20秒（含启动浏览器）
- 如微信升级反爬策略，需更新UA和反检测配置
- 实测成功案例：抓取5641字全文 ✅

### 关键反检测配置
1. 自定义UserAgent（伪装Mac Safari）
2. 隐藏`navigator.webdriver`标识
3. 设置中文locale + 上海时区
4. viewport 1920x1080

---

## ⚠️ 公众号内容红线（2026-03-01 金主人确认）

**绝对禁止写央企相关内容！** 金主人在央企（中国人寿财险）的工作内容需要保密，公众号文章不得涉及：
- 具体公司名称、业务数据
- 内部项目细节（如智能审核系统）
- 任何可追溯到具体央企的案例

**12,681次审核、37家分公司等数据仅限内部材料使用，不得出现在公众号。**
