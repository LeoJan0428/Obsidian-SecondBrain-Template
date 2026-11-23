# AgentOS 推薦開發工作流 (Recommended Workflow)

本文件定義了使用 AI Agent 進行新需求或專案開發時的標準工程流水線（Pipeline）。這套流程整合自 `mattpocock/skills`，能有效防止 AI 瞎猜需求或寫出無法維護的程式碼。

---

## 🔄 標準工程流水線 (The AgentOS Pipeline)

```
[ Phase 1: 需求釐清 ] ──> [ Phase 2: 架構與規格 ] ──> [ Phase 3: 任務拆解 ]
   /grill-with-docs              /to-spec                   /to-tickets
                                                                 │
[ Phase 6: 上下文交接 ] <── [ Phase 5: 代碼審查 ] <── [ Phase 4: TDD 實作 ]
     /handoff                  /code-review             /implement + tdd
```

---

## 階段說明與呼叫技能

### Phase 1: 需求釐清 (`/grill-with-docs`)
* **目標**：透過蘇格拉底式問答，釐清邊界條件、非功能需求與可能陷阱。
* **觸發方式**：當使用者提出新 Idea 或新需求時。
* **成果**：產出點子草稿與邊界共識。

### Phase 2: 架構與規格 (`/to-spec`)
* **目標**：將討論出的需求轉化為正式的 `SPEC.md` 文件。
* **成果**：包含架構圖、API 介面定義、資料結構的 `SPEC.md`。

### Phase 3: 任務拆解 (`/to-tickets`)
* **目標**：將 `SPEC.md` 拆解為可增量測試與實作的獨立 `TICKETS.md`。
* **成果**：按依賴順序排列的微型任務清單。

### Phase 4: 實作與測試 (`/implement` & `tdd`)
* **目標**：依照 Ticket 順序進行開發，採用 Test-Driven Development (Red-Green-Refactor)。
* **原則**：先寫會失敗的測試，再編寫最低限度代碼使其通過，最後重構。

### Phase 5: 代碼與架構審查 (`/code-review`)
* **目標**：從代碼品質、安全、規範及規格一致性進行雙軸度審查。

### Phase 6: 上下文交接 (`/handoff`)
* **目標**：任務完成或階段結束時，更新專案的 `CONTEXT.md`，壓縮與清理對話 Context。
