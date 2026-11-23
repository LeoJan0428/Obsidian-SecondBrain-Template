# AGENT_GUIDE.md: AI Agent 統一導覽與操作手冊 (v3.0)

> [!IMPORTANT]
> **本手冊定位：AgentOS 工作流執行與提問模板 SOP**  
> 全域核心鐵律（單倉自包含 + 全域 AgentOS、反迎合求真、條件式遙測、強制外檢、50/60 行上限）請以根目錄 [**AGENTS.md**](../AGENTS.md) 為唯一事實來源。

---

## ⚡ 1. 工作流三級分流決策矩陣 (Workflow Triage Matrix)

| 任務層級 | 判定特徵 | 強制流轉路徑 | 必要產出與限制 |
| :--- | :--- | :--- | :--- |
| **L1【微型維護】** | • `< 30 行` 代碼變更<br/>• 數值微調、Typo、文檔小修 | 讀專案 `AGENTS.md` $\to$ `implement` $\to$ 本地驗證 $\to$ `commit` | • 免 SPEC / TICKETS<br/>• 免 `[GATE]` / `[RETRIEVAL_PROOF]` |
| **L2【常規功能 / 除錯】** | • 新增單一模組功能<br/>• 明確 Bug 修復<br/>• 單一 Ticket 推進 | 讀 `AGENTS.md` + `TICKETS.md` $\to$ `tdd` $\to$ `implement` $\to$ `commit` $\to$ `/handoff` | • 輸出 `[GATE]` 與 `[RETRIEVAL_PROOF]`<br/>• 同步 `CONTEXT.md` |
| **L3【新專案 / 跨模組重構】** | • 全新專案啟動<br/>• 跨模組架構重組<br/>• 核心演算法 / 技術選型 | **觸發顆粒度熔斷** $\to$ 確認拆解後走滿標準 **8 階工作流** | • 產出/更新四件套<br/>• 雙軸度 `code-review` |

---

## 🛠️ 2. L3 標準 8 階工程工作流 (Standard 8-Stage Workflow)

```mermaid
flowchart TD
    A[使用者 Idea / 重大架構變更] --> B[/grill-with-docs<br/>蘇格拉底提問與文檔對齊]
    B --> C[/to-spec<br/>生成 SPEC.md + 冷啟動專案 AGENTS.md]
    C --> D[/to-tickets<br/>拆解 Given/When/Then 微工單]
    D --> E[/tdd<br/>先寫紅燈測試與契約斷言]
    E --> F[/implement<br/>鎖定單一 Ticket 綠燈實作與重構]
    F --> G[/code-review<br/>標準與架構雙軸度審查]
    G --> H[原子化 Commit<br/>專案倉儲獨立提交與 PR/CI 閉環]
    H --> I[/handoff<br/>更新 CONTEXT.md 與知識升遷]
```

### 階段職責與關鍵守門：
1. **`/grill-with-docs`**：結合 `02-Areas/` 既有筆記進行挑戰式提問，釐清架構邊界與隱含假設。
2. **`/to-spec`**：產出 `./SPEC.md`，並同步從 `05-Templates/Project_AGENTS_Template.md` 冷啟動專案根目錄 `./AGENTS.md` 初版。
3. **`/to-tickets`**：將 `SPEC.md` 拆解為獨立、具 Given/When/Then 驗收條件的 `TICKETS.md`。
4. **`/tdd` $\to$ `/implement`**：嚴格先紅燈後綠燈，鎖定單一 Ticket 範圍，嚴禁順手改動無關檔案。
5. **`/code-review`**：從標準面、規格面、架構依賴與資源生命週期雙軸審查。
6. **`commit`**：於專案倉儲（`<WORKSPACE_ROOT>/repos/<專案>/`）獨立原子提交（僅舊版解耦專案需雙邊提交）；禁 `git add .`，交由全域 `00-AgentOS/hooks/` 自動守門。
7. **`/handoff`**：執行知識升遷（`CONTEXT.md` $\to$ `AGENTS.md` / `SPEC.md` / `02-Areas/`）、修剪滾動視窗並壓縮上下文。

> 💡 **外檢前置硬阻斷**：進入架構設計或技術選型前，凡涉及業界實務、第三方庫或報錯，必須先調用 `web-research` 技能（遵循 `[AGENTS.md]` §3 硬阻斷）。  
> 完整技能實體置於 `00-AgentOS/skills/`，透過 Windows Junction 映射至 `.agents/skills`、`.claude/skills`、`.cursor/skills`。

---

## 📏 3. 50/60 行雙滾動窗口與知識升遷

1. **專案 `AGENTS.md` ($\le 50$ 行)**：僅收錄 `MUST`/`NEVER` 領域鐵律、模組邊界與驗證指令。逼近上限時，將可自動化條款**固化為 Linter / 型別 / 測試斷言**後精簡文字。
2. **專案 `CONTEXT.md` ($\le 60$ 行)**：必須於 Frontmatter 標明 `repo_path`；已完成事項（Done）**僅保留最近 3 筆**，淘汰前須先執行知識升遷，歷史交由 Git Log 封存。

---

## 💬 4. 使用者提問模板響應準則

* **模板 A（新專案 / 新 Idea）**：先檢索 `02-Areas/` 既有知識 $\to$ 執行 `/grill-with-docs` 提出 3–5 個架構邊界與 Trade-off 問題 $\to$ 確認後於 `repos/<專案>/` 單倉建立程式碼與治理四件套（無須建立 `.code-workspace`）。
* **模板 B（既有專案推進 / 除錯）**：判定 L1/L2 $\to$ 執行 30 秒 Fast Onboarding（讀 `AGENTS.md` + `CONTEXT.md`）$\to$ 確認目標 Ticket $\to$ TDD 優先。
* **模板 C（重大架構決策 ADR）**：先啟動 `web-research` 查證 $\to$ 依 `05-Templates/Decision_Template.md` 產出 ADR $\to$ 術語參照 `00-AgentOS/GLOSSARY.md`。
* **收尾指令（`/handoff`）**：依 `00-AgentOS/skills/handoff/SKILL.md` 完成升遷、50/60 行校驗與跨機同步檢查。

---

## 📁 5. 單倉自包含與專案生命週期

詳見 [workflows/PROJECT_LIFECYCLE.md](./workflows/PROJECT_LIFECYCLE.md)：

| 位置 | 定位 | 內容規範 |
| :--- | :--- | :--- |
| **`<WORKSPACE_ROOT>/repos/<專案>/`** | **自包含專案倉儲（預設）** | 同置原始碼、測試、`.github/workflows/ci.yml` 與治理四件套（公開倉須將 `CONTEXT.md` / `TICKETS.md` 加入 `.gitignore`） |
| **`Obsidian-SecondBrain-Template/`（`02-Areas/`、`00-AgentOS/`）** | **長青知識與全域 AgentOS** | 跨專案長青筆記、全域技能與 Hooks 唯一來源（經 `~/.gemini/config/` 全域掛載至所有專案）及舊版專案紀錄 |
| **`04-Archive/projects/<專案>/`** | **統一結案封存區** | 結案時產出 `SUMMARY.md` 並標記 `status: archived`，釋放活躍區注意力 |
