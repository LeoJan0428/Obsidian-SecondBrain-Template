---
name: implement
description: 執行特定 Ticket 的開發實作，自動觸發 tdd 測試流程。
---

# Skill: implement

## 目的
安全、標準地執行 `TICKETS.md` 中的當前任務。

## 執行步驟
1. 讀取專案 `AGENTS.md`、`CONTEXT.md` 與 `TICKETS.md` 中優先度最高的卡片。
2. **依階段選擇實作模式**：
   - **L2 / L3 Expand・Extract 期**：強制呼叫 `tdd` 技能進行開發（紅燈測試 $\to$ 最小實作 $\to$ 驗證與重構）。
   - **Explore 原型探索期**：依 `00-AgentOS/PROFILE.md`（`GLOBAL-01`）採極簡驗證，不預先強制重型測試與過度抽象。
3. 完成後更新 `TICKETS.md` 狀態為已完成並執行專案驗證指令。
