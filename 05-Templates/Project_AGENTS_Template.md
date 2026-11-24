@./CONTEXT.md

# [DOMAIN-CODEX] 專案領域法典：{{title}}

> [!IMPORTANT]
> **四件套導航**：**領域法典 (本檔)** ｜ [工作暫存](./CONTEXT.md) ｜ [系統藍圖](./SPEC.md) ｜ [執行佇列](./TICKETS.md)  
> **全域憲法**：經 `~/.gemini/config/AGENTS.md` 自動繼承（SSOT 位於 `<WORKSPACE_ROOT>/Obsidian-SecondBrain-Template/AGENTS.md`）。  
> **程式碼倉儲**：`<WORKSPACE_ROOT>/repos/{{title}}`（單倉自包含開發；不須 `.code-workspace`）  
> **單向收緊鐵律**：僅能附加更嚴格之領域約束，嚴禁放寬全域憲法之測試、Git 衛生與 **本檔 $\le 50$ 行 / CONTEXT $\le 60$ 行** 硬上限。

<!-- [AGENT-INIT-RULE]: 冷啟動時僅填寫已確定之技術棧物理邊界（2~3 條），嚴禁填寫 Clean Code/PEP8 等通用廢話。總長嚴格 <= 50 行。 -->

## 1. 架構拓撲與路徑邊界 (Architecture & Path Boundaries)
- **[ARCH-01 技術棧與環境]**：`<填寫語言與核心框架版本，例：Python 3.10 + FastAPI / Kotlin 1.9 + OpenCV 4.9>`
- **[ARCH-02 模組單向依賴]**：`<填寫依賴方向，例：presentation -> application -> domain；domain 層嚴禁 import 外部 I/O 框架>`
- **[ARCH-03 資料與快取隔離]**：**嚴禁** 讀取或檢索 `<填寫禁入路徑，例：data/ 或外部資料湖>`；結構對照一律僅讀取 `tests/fixtures/`。

## 2. 領域與資源絕對不變量 (Domain & Resource Invariants)
- **[INV-01 核心業務唯一真理源]**：`MUST` `<填寫核心計算或狀態委派對象>`；`NEVER` `<填寫禁止硬編碼或繞過之行為>`。
- **[INV-02 資源生命週期與並行護欄]**：`MUST` `<填寫記憶體釋放、執行緒派發或硬體安全底線>`；`NEVER` `<填寫會導致 OOM/Race Condition 之禁忌>`。
<!-- [PROMOTION-ANCHOR]: /handoff 知識升遷時，將新發現之 API/硬體踩坑提煉為 1 行 [INV-0X] 插入於此錨點上方（上限 8 條；滿額時須固化為測試或 Linter 並精簡舊條文）。 -->

## 3. 本地確定性驗證閘門 (Deterministic Verification Gate)
提交任何 Commit 或執行 `/handoff` 前，必須於專案 Code Repo 根目錄執行以下指令且 Exit Code 必須為 `0`：
- **L1 單檔極速驗證**：`<例：pytest tests/test_target.py -q --maxfail=1>`
- **L2/L3 完整測試與靜態檢查**：`<例：ruff check . && mypy src/ && pytest tests/ -q>`
