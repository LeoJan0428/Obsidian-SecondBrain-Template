# GLOSSARY.md: Shared Language & Technical Terms (共享術語庫)

> [!IMPORTANT]
> **Token 節省約束**：  
> 當 AI Agent 在對話或筆記中提及以下名詞時，**必須直接引用本檔案中的定義或使用連結（例：`[[GLOSSARY#MCP|MCP]]`）**，嚴禁在對話中花費 Context Token 重覆解釋已知概念。

---

## 🤖 AI & Agent 領域

### Agent (AI 代理)
* **定義**：具有自決自主權（Autonomy）、配備工具（Tools）並能依據目標（Goals）進行規劃與自我修正的 LLM 執行實體。

### AgentOS (代理作業系統)
* **定義**：在 SecondBrain 知識庫中運行的工作流規範與技能架構（整合自 mattpocock/skills），規範 Agent 的開發步驟（Grill $\rightarrow$ Spec $\rightarrow$ Tickets $\rightarrow$ TDD $\rightarrow$ Review）。

### Context Window (上下文視窗)
* **定義**：LLM 單次推論可處理的最大 Token 數量。本系統透過 `CONTEXT.md` 實施分層載入（Lazy Context Loading），以最小化 Context 佔用。

### Memory (代理記憶)
* **短期記憶**：當前對話歷史與載入的 `CONTEXT.md`。
* **長期記憶**：Obsidian `SecondBrain/` 檔案庫與 `Smart Connections` 本地向量索引。

### Tool Call / Function Calling (工具呼叫)
* **定義**：LLM 輸出特定 JSON 結構以調用外部 API、執行 Shell 指令或讀寫檔案的能力。

---

## 🔍 RAG & Vector DB 領域

### MCP (Model Context Protocol)
* **定義**：由 Anthropic 提出的開放標準協定，用於在 AI 模型與資料庫、本地工具、SaaS 服務之間建立安全的雙向上下文連接。

### RAG (Retrieval-Augmented Generation / 檢索增強生成)
* **定義**：透過外部資料庫檢索相關文檔片段（Chunks），並作為 Prompt 注入 LLM 以提高回答準確度並減少幻覺（Hallucination）。

### Vector DB / Embedding (向量資料庫與嵌入)
* **定義**：將文字轉換為高維向量（Vector）並計算餘弦相似度（Cosine Similarity），用於語意搜尋。本知識庫使用 `Smart Connections` 進行本地端 Embedding 索引。

---

## ⚙️ 軟體工程與開發流程

### TDD (Test-Driven Development / 測試驅動開發)
* **定義**：遵循 Red-Green-Refactor 循環。先撰寫會失敗的單元測試，再寫最低限度的實現程式碼使測試通過，最後進行重構。

### PRD (Product Requirements Document / 產品需求文件)
* **定義**：描述產品功能、目標使用者、成功指標與核心邏輯的高階需求說明檔。

### Spec (Technical Specification / 技術規格書)
* **定義**：描述技術實作細節、資料結構、API 介面與架構圖的技術設計文件。

### Ticket (任務卡片)
* **定義**：可獨立完成、符合 Tracer-Bullet 原則的微型開發任務。

---

## 🧠 知識管理與系統

### WikiLinks (Obsidian 雙向連結)
* **定義**：`[[Note Name]]` 格式。用於在 SecondBrain 中建立原子筆記之間的語意網格，方便 Smart Connections 計算關聯度。

### Lazy Context Loading (分層加載)
* **定義**：Agent 先讀取 30 秒 `CONTEXT.md`，僅在需要時才讀取深層文檔與程式碼，避免一次載入過多背景資料。

---

## 📈 大數據分析與量化金融 (Data Analysis & Quantitative Finance)

### Alpha vs. Beta (超額收益與市場基準收益)
* **Beta ($\beta$)**：與大盤市場同步波動所獲得的基準回報（市場系統性風險補償）。
* **Alpha ($\alpha$)**：透過主動策略、因子模型或微觀定價偏差所獲得的、與大盤無關的純粹超額回報。

### Sharpe Ratio (年化夏普比率)
* **定義**：衡量承擔每單位總風險所獲得的超額回報：$SR = \frac{E[R_p - R_f]}{\sigma_p} \times \sqrt{252}$。實盤策略通常要求 $SR > 1.5$。

### Maximum Drawdown (MDD / 最大回撤)
* **定義**：歷史資產淨值曲線自任意最高峰至最低谷的最大虧損幅度，衡量策略最極端的下行風險承受度。

### Lookahead Bias (未來函數 / 前視偏差)
* **定義**：回測計算時誤用了未來才發生的數據（如用 T 日收盤價作為 T 日開盤訊號）。本系統強制使用 `.shift(1)` 遞延消除此偏差。

### Multi-Factor Model (多因子模型)
* **定義**：將股票收益分解為價值 (Value)、動量 (Momentum)、品質 (Quality)、低波動 (Low Vol) 與規模 (Size) 等維度進行量化打分之投資框架。

