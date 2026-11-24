# 🧠 SecondBrain (AI-Native Knowledge OS)

本系統採用 **單倉自包含 + 全域 AgentOS 掛載架構**：各專案程式碼與治理文件同置於獨立 Git 倉儲，無須維護繁瑣的多根工作區；Obsidian 知識庫專注於跨專案長青筆記（`02-Areas/`）並作為全域規則、14 大技能與 Git 安全 Hooks 的唯一事實來源（SSOT），透過 `~/.gemini/config/` 自動套用至本機所有獨立專案。

---

## 🏗️ 實體目錄拓撲 (Self-Contained + Global AgentOS Layout)

```text
<WORKSPACE_ROOT>/
├── Obsidian-SecondBrain-Template/         # 跨專案長青知識庫 + 全域 AgentOS (Skills / Hooks / AGENTS.md)
│   ├── AGENTS.md                    # 全域憲法 (v3.0)，同步連結至 ~/.gemini/config/AGENTS.md
│   ├── 00-AgentOS/                  # Skills / Hooks / Workflows / PROFILE / GLOSSARY
│   ├── 02-Areas/                    # 跨專案長青知識資產
│   │   └── Software-Architecture/   # 跨專案系統架構模式庫與避坑清單
│   └── setup_skills_junctions.bat   # Windows 一鍵全域掛載腳本
└── repos/                           # 各專案獨立自包含 Git 倉儲
    └── <專案>/                      # 直接同置程式碼、AGENTS.md、CONTEXT.md、SPEC.md、TICKETS.md 與 ci.yml
```

---

## ⚡ 跨裝置 Agent 快速開箱建置 (Cross-Device Bootstrap)

詳細步驟教學請參閱 **[SETUP.md](./SETUP.md)**。

### 步驟 1：一鍵建立技能掛載、全域規則與 Git 安全防線
在 Windows 終端於本庫根目錄執行（自動設定全域 `core.hooksPath` 金鑰攔截、UTF-8 路徑，並將規則與 14 大技能映射至 `.agents`、`.claude`、`.cursor` 與 `%USERPROFILE%\.gemini\config\`）：
```cmd
.\setup_skills_junctions.bat
```

### 步驟 2：安裝開發驗證與 GitHub PR/CI 工具（選配）
```bash
pip install ruff pytest pytest-archon deptry
winget install --id GitHub.cli -e --accept-package-agreements --accept-source-agreements
gh auth login
```

### 步驟 3：啟動開發（直接開啟單一專案資料夾）
1. 在 IDE、桌面 App 或 `agy` CLI **直接開啟 `<WORKSPACE_ROOT>/repos/<專案>/`**，全域規範、14 大技能與 Git 金鑰防線自動生效。
2. 專案內若包含治理四件套，Agent 依 `AGENTS.md`（$\le 50$ 行）與 `CONTEXT.md`（$\le 60$ 行）完成 30 秒 Fast Onboarding；若為公開倉儲，將 `CONTEXT.md`、`TICKETS.md` 等私人工作檔列入 `.gitignore` 即可。

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
| **`grill-with-docs`** | **蘇格拉底式提問與需求對齊**（優先路由架構模式卡與避坑清單，挑戰需求邊界） | `/grill-with-docs` | 知識庫架構路由 |
| **`to-spec`** | **產出 SPEC.md（含架構模式與 ADR 取捨）並同步冷啟動專案 `AGENTS.md`** | `/to-spec` | Markdown |
| **`to-tickets`** | **將 SPEC 拆解為 Given/When/Then 微型工單** | `/to-tickets` | Markdown |
| **`handoff`** | **知識升遷、50/60 行雙上限校驗與 `CONTEXT.md` 交接** | `/handoff`、20+ 輪防衰退 | Git Log, `CONTEXT.md` |
| **`ask-matt`** | **AgentOS 技能與系統架構諮詢助手** | `/ask-matt` | 知識庫參照 |

---

## 📚 系統核心文件導覽

* 🤖 **AI Agent 核心規範**：[AGENTS.md](./AGENTS.md) ｜ [00-AgentOS/AGENT_GUIDE.md](./00-AgentOS/AGENT_GUIDE.md) ｜ [00-AgentOS/PROFILE.md](./00-AgentOS/PROFILE.md)
* 🏗️ **系統架構模式庫**：[02-Areas/Software-Architecture/README.md](./02-Areas/Software-Architecture/README.md) ｜ [05-Templates/Architecture_Playbook_Template.md](./05-Templates/Architecture_Playbook_Template.md)
* 🧭 **每日決策看板**：[DASHBOARD.md](./DASHBOARD.md) ｜ [PROJECTS_WAR_ROOM.canvas](./PROJECTS_WAR_ROOM.canvas)
* 🛠️ **Obsidian 與環境開箱**：[SETUP.md](./SETUP.md) ｜ [UserGuide/SETUP_GUIDE.md](./UserGuide/SETUP_GUIDE.md)
* 👤 **人類操作手冊與元件說明**：[UserGuide/USER_GUIDE.md](./UserGuide/USER_GUIDE.md) ｜ [UserGuide/SYSTEM_COMPONENTS.md](./UserGuide/SYSTEM_COMPONENTS.md)
