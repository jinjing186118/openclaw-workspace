# 微信公众号文章抓取策略（全Bot必读）

_更新日期：2026-03-02 | 来源：金主人指示_

## 🚨 核心规则

**遇到微信公众号链接（mp.weixin.qq.com），必须按以下流程执行：**

```
Step 1: 先用 web_fetch 尝试抓取
Step 2: 如果 web_fetch 返回内容不足（<200字或只有公众号名称）
       → 立即自动降级到 Playwright 方案
       → 不要回复用户说"抓不到"
       → 不要让用户截图或复制粘贴
Step 3: 用 Playwright 抓取（命令见下方）
Step 4: 返回完整内容
```

## ❌ 绝对不能做的事

- 告诉用户"微信文章抓不到"
- 让用户截图或复制内容
- 让用户反复提醒你去找方案

## Playwright 抓取命令

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

## 详细技术文档

参见：`memory/wechat-article-scraping.md`（各workspace均有副本）
