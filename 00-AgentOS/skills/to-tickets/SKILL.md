---
name: to-tickets
description: 將 SPEC.md 拆解為可獨立執行的微型任務卡片 (TICKETS.md)。
---

# Skill: to-tickets

## 目的
將大塊技術規格拆解為「原子化卡片」，讓 Agent 每次專注於單一小任務並以確定性條件驗收。

## 執行步驟
1. 讀取 `./SPEC.md`（舊版解耦專案則讀 `01-Projects/_active/<Project>/SPEC.md`）。
2. 將任務拆解為可獨立實作與測試的卡片，寫入專案根目錄 `./TICKETS.md`。
3. 每個 Ticket 必須包含：
   - `[ ] Ticket-ID: 標題`
   - **依賴項 (Dependencies)** 與 **影響範圍 (Scope)**
   - **驗收條件 (Given / When / Then)**：具體可測之前置條件、動作與預期結果／驗證指令。
