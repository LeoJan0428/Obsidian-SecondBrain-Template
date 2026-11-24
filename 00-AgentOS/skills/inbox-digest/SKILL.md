---
name: inbox-digest
description: 靈感收集箱自動消化、外部文章提煉與長青知識升遷技能 (Inbox Digest & Knowledge Ingestion Pipeline)。
---

# Skill: inbox-digest

## 目的
將 `_inbox/` 收集箱中的零散文章、Web Clipper 剪藏、隨手靈感或代碼片段，自動提煉為高品質的原子筆記，精準歸檔至 `02-Areas/` 或 `03-Resources/`，並自動建立雙向連結與索引，防止靈感堆積成資訊墳場。

---

## 核心原則 (Core Principles)

1. **原子化原則 (Atomicity)**：
   - 一篇長文提煉出 1~3 個獨立的原子核心概念，而非整篇無腦複製。
   - 每篇原子筆記專注解決一個問題或記錄一個架構模式。
2. **長青升遷導航 (Evergreen Routing)**：
   - 涉及領域長期知識（如台股多因子、XAI 歸因、影像處理數學、機器人運動學）$\to$ 提煉寫入 `02-Areas/[對應領域]/`。
   - 涉及外部參考手冊、論文摘要、工具 CheatSheet $\to$ 歸入 `03-Resources/`。
   - 涉及某活躍專案的具體靈感 $\to$ 整理後直接加入該專案的 `TICKETS.md` 或 `SPEC.md`。
3. **雙向連結織網 (Backlink Weaving)**：
   - 產出的原子筆記必須至少與 1 篇 `02-Areas/` 的核心主題或 `GLOSSARY.md` 建立連結。
4. **收件箱清零 (Inbox Zero)**：
   - 提煉完成後，將 `_inbox/` 內的原檔歸檔至 `04-Archive/inbox_archive/` 或在確認無遺漏後清理，保持 `_inbox/` 極度清爽。

---

## 執行流程 (Execution Steps)

1. **掃描收件箱**：
   - 檢索 `_inbox/` 下除了 `README.md` 以外的所有 Markdown 檔案。
2. **內容解析與分流**：
   - 提取每篇筆記的「核心論點」、「可重用代碼」與「技術啟發」。
   - 濾除廢話、廣告與 SEO 冗贅詞。
3. **原子筆記生成**：
   - 依照 `05-Templates/Knowledge_Template.md` 生成結構化筆記。
   - 補齊統一 YAML Frontmatter（`title`、`type: concept`、`category`、`domain`、`tags`、`last_updated`）。
4. **歸檔與收尾**：
   - 移出已消化的原始檔案，更新相關 Index 筆記。
   - 輸出消化簡報，列出本次新增的長青知識卡片。
