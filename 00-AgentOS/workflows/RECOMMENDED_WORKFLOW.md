# AgentOS 推薦開發工作流 (Recommended Workflow)

本文件說明 AgentOS 的標準 **L3 8 階工程流水線**；任務規模分流（L1 / L2 / L3 決策矩陣）請參閱 [AGENT_GUIDE.md](../AGENT_GUIDE.md)，Explore 原型期豁免規則見 [PROFILE.md](../PROFILE.md)（`GLOBAL-01`）。

---

## 🔄 標準 8 階工程流水線 (The 8-Stage Pipeline)

```text
[1. 需求釐清] /grill-with-docs ──> [2. 規格與法典] /to-spec ──> [3. 微工單拆解] /to-tickets
                                                                         │
[4. 紅燈測試] /tdd ──> [5. 綠燈實作] /implement ──> [6. 雙軸審查] /code-review
                                                                         │
[8. 知識交接] /handoff <── [7. 原子提交 & PR/CI 閉環] git commit / gh pr checks
```

---

## 階段說明與呼叫技能

### 1. 需求釐清 (`/grill-with-docs`)
* 檢索 `02-Areas/` 既有筆記，以蘇格拉底式問答釐清邊界條件、非功能需求與架構陷阱。

### 2. 架構與規格 (`/to-spec`)
* 收斂產出 `SPEC.md`（架構、Schema、狀態機與公式），並同步冷啟動專案 `./AGENTS.md`（$\le 50$ 行）與 `./CONTEXT.md`（$\le 60$ 行）。

### 3. 任務拆解 (`/to-tickets`)
* 將 `SPEC.md` 拆解為按依賴排列、具 `Given / When / Then` 驗收條件的微型任務卡片 `TICKETS.md`。

### 4. 紅燈測試 (`/tdd`)
* 依 Ticket 驗收條件先寫會失敗的契約或單元測試（Red），確認測試真正覆蓋預期行為。

### 5. 綠燈實作與重構 (`/implement`)
* 鎖定單一 Ticket 編寫最小實作使測試通過（Green），並在全綠前提下進行重構（Refactor）。

### 6. 代碼與架構雙軸審查 (`/code-review`)
* 從 **標準面**（Lint、型別、安全、資源生命週期、例外衛生）與 **規格面**（`SPEC.md` / `TICKETS.md` / `AGENTS.md` 不變量）雙軸檢核。

### 7. 原子化提交與 PR/CI 閉環 (`commit` + `gh pr`)
* 精確 `git add <path>`（禁 `git add .`），由全域 `00-AgentOS/hooks/` 守門；若具 GitHub Remote 與 CI，開功能分支推送建 PR 並監看至全綠燈（嚴禁自動 Merge）。

### 8. 上下文交接 (`/handoff`)
* 執行知識升遷（`CONTEXT.md` $\to$ `AGENTS.md` / `SPEC.md` / `02-Areas/`）、50/60 行雙上限校驗並更新下一步行動。
