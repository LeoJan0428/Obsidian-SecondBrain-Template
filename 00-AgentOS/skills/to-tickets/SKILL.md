---
name: to-tickets
description: 將 SPEC.md 拆解為可獨立執行的微型任務卡片 (TICKETS.md)。
---

# Skill: to-tickets

## 目的
將大塊技術規格拆解為「原子化卡片」，讓 Agent 每次專注於單一小任務，確保進度可追蹤。

## 執行步驟
1. 讀取 `SPEC.md`。
2. 將任務拆解為短小、具體、可驗證的卡片，寫入 `TICKETS.md`。
3. 每個 Ticket 格式：
   - `[ ] Ticket-ID: 標題`
   - **驗證條件 (Acceptance Criteria)**
   - **依賴項 (Dependencies)**
