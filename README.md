# 🧠 SecondBrain (AI-Native Knowledge OS)

本系統採用 **Code-Vault 解耦架構**：Obsidian 知識庫作為純 Markdown 治理中心與大腦記憶，獨立程式碼倉儲透過 Multi-Root Workspace (`.code-workspace`) 協同開發，搭配 `00-AgentOS` 技能庫與本地 Git Hooks 自動守門。

---

## 🏗️ 實體目錄拓撲 (Code-Vault Decoupled Layout)

```text
<WORKSPACE_ROOT>/
├── Obsidian-SecondBrain-Template/   # 純 Markdown 知識庫 (Vault + AgentOS + 專案治理四件套 SSOT)
│   ├── AGENTS.md                    # 全域憲法 (v3.0)
│   ├── 00-AgentOS/                  # Skills / Hooks / Workflows / PROFILE / GLOSSARY
│   └── 01-Projects/_active/<專案>/  # 僅存四件套：AGENTS.md, CONTEXT.md, SPEC.md, TICKETS.md
├── repos/                           # 各專案獨立程式碼 Git 倉儲（不含巢狀 Submodule 地獄）
│   └── <專案>/
└── workspaces/                      # 一鍵多根開發工作區（同時掛載 Code Repo + Vault）
    └── <專案>.code-workspace
```

---

## ⚡ 跨裝置 Agent 快速開箱建置 (Cross-Device Bootstrap)

### 步驟 1：建立技能目錄鏈結與 Git Hooks
在 Windows 終端於本庫根目錄執行（自動設定 `core.hooksPath`、UTF-8 路徑，並將 `00-AgentOS/skills` 映射至 `.agents`、`.claude`、`.cursor`）：
```cmd
.\setup_skills_junctions.bat
```

### 步驟 2：安裝全域診斷與測試工具
```bash
pip install ruff pytest pytest-archon deptry
```

### 步驟 3：啟動開發（Multi-Root Workspace）
1. 打開對應專案的 `<WORKSPACE_ROOT>/workspaces/<專案>.code-workspace`（同時載入程式碼倉儲與知識庫）。
2. Agent 依根目錄 **[AGENTS.md](./AGENTS.md)** 執行 30 秒 Fast Onboarding：讀取該專案 `01-Projects/_active/<專案>/AGENTS.md`（$\le 50$ 行）與 `CONTEXT.md`（$\le 60$ 行）。

---

## 🛠️ 現役 AgentOS 全域技能清冊 (14 Active Skills)

所有技能原始檔集中於 `00-AgentOS/skills/`，新增或異動技能時強制同步更新本表：

| 技能名稱 (Skill Name) | 核心職責與定位 | 觸發方式 / 指令 | 必備底層依賴工具 |
| :--- | :--- | :--- | :--- |
| **`web-research`** | **外部事實查證、業界最新標準調研與第三方規範檢索**（強制第一動作聯網） | 業界實務、API 查詢、報錯排查 | `search_web` |
| **`inbox-digest`** | **靈感收集箱自動消化、外部文章提煉與長青知識升遷**（`_inbox/` $\to$ `02-Areas/`） | 「整理收件匣」、「消化剪藏」 | Markdown, `_inbox/` |
| **`code-simplify`** | **專案代碼簡化、死代碼掃除與抗腐化**（拆解上帝物件，行為等價） | 「簡化專案」、「清理死代碼」 | `ruff`, `pytest-archon` |
| **`doc-cleanup`** | **知識庫文檔抗腐化、歷史研報歸檔與 Markdown 一致性稽核** | 「整理過期文檔」、「歸檔研報」 | Markdown, Git Log |
| **`tech-debt-audit`** | **技術債全面體檢、架構腐化審查與例外黑洞排查** | `/tech-debt-audit`、「技術債健檢」 | `ruff`, `pytest-archon` |
| **`dep-clean`** | **依賴庫瘦身、幽靈套件排查與 requirements.txt 自動校準** | 「檢查依賴套件」、「依賴減肥」 | `deptry` |
| **`tdd`** | **測試驅動開發核心流程**（紅燈 $\to$ 綠燈 $\to$ 重構） | `/tdd`、功能與修復開發 | `pytest` |
| **`implement`** | **鎖定單一工單執行實作**（自動帶動 TDD 循環） | `/implement <Ticket>` | 專案測試套件 |
| **`code-review`** | **代碼變更雙軸度審查**（標準面 + 規格面） | `/code-review`、提交前檢核 | Git Diff, Linter |
| **`grill-with-docs`** | **蘇格拉底式提問與需求對齊**（挑戰需求邊界） | `/grill-with-docs` | 知識庫檢索 |
| **`to-spec`** | **產出 SPEC.md 並同步冷啟動專案 `AGENTS.md`** | `/to-spec` | Markdown |
| **`to-tickets`** | **將 SPEC 拆解為 Given/When/Then 微型工單** | `/to-tickets` | Markdown |
| **`handoff`** | **知識升遷、50/60 行雙上限校驗與 `CONTEXT.md` 交接** | `/handoff`、20+ 輪防衰退 | Git Log, `CONTEXT.md` |
| **`ask-matt`** | **AgentOS 技能與系統架構諮詢助手** | `/ask-matt` | 知識庫參照 |

---

## 📚 系統核心文件導覽

* 🤖 **AI Agent 核心規範**：[AGENTS.md](./AGENTS.md) ｜ [00-AgentOS/AGENT_GUIDE.md](./00-AgentOS/AGENT_GUIDE.md) ｜ [00-AgentOS/PROFILE.md](./00-AgentOS/PROFILE.md)
* 🧭 **每日決策看板**：[DASHBOARD.md](./DASHBOARD.md) ｜ [PROJECTS_WAR_ROOM.canvas](./PROJECTS_WAR_ROOM.canvas)
* 🛠️ **Obsidian 與環境開箱**：[SETUP.md](./SETUP.md) ｜ [UserGuide/SETUP_GUIDE.md](./UserGuide/SETUP_GUIDE.md)
* 👤 **人類操作手冊與元件說明**：[UserGuide/USER_GUIDE.md](./UserGuide/USER_GUIDE.md) ｜ [UserGuide/SYSTEM_COMPONENTS.md](./UserGuide/SYSTEM_COMPONENTS.md)
