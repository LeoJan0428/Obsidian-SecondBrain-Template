# Project Lifecycle & Token Management Protocol (v3.0)

本文件說明專案在 SecondBrain（單倉自包含 + 全域 AgentOS 掛載架構）中的生命週期流轉與 Token 控管法則。

---

## 📁 專案生命週期兩態流轉（單一封存真源）

1. **活躍開發區（預設）：`<WORKSPACE_ROOT>/repos/<ProjectName>/`**
   - 程式碼、測試、`.github/workflows/ci.yml` 與治理四件套（`AGENTS.md` $\le 50$ 行、`CONTEXT.md` $\le 60$ 行、`SPEC.md`、`TICKETS.md`）直接同置於單一 Git 倉儲，無須建立 `.code-workspace`。
   - 若專案預計設為 Public，請將 `CONTEXT.md`、`TICKETS.md` 加入 `.gitignore`；舊版存放於 `01-Projects/_active/<ProjectName>/` 的歷史專案仍維持相容。

2. **統一封存區：`04-Archive/projects/<ProjectName>/`**
   - 已結案或不再維護的專案，統一移入 `04-Archive/projects/`（不再另設 `01-Projects/_archive/`，確保全庫單一 Archive 真源）。
   - 封存 SOP：
     1. 產出 `SUMMARY.md`（結案成果、關鍵技術資產與 `repo_path`）。
     2. 將 `CONTEXT.md` Frontmatter 標記為 `status: archived`。
     3. 移出 `01-Projects/_active/`（自動從 `DASHBOARD.md` 活躍矩陣移除，釋放注意力）並同步精簡 `PROJECTS_WAR_ROOM.canvas`。
     4. 對應程式碼倉儲保留於 `repos/<ProjectName>/`，隨時可零損還原。

---

## 💰 Token 控管四大法則

1. **30 秒 Fast Onboarding**：切換專案先讀 `AGENTS.md` + `CONTEXT.md`（$\le 110$ 行），嚴禁盲目全庫掃描。
2. **按需載入**：僅在 L2/L3 涉及架構與拆解時讀取 `SPEC.md` / `TICKETS.md`，參考知識僅取最相關 2–3 篇。
3. **20+ 輪主動 `/handoff`**：執行知識升遷與 50/60 行修剪，防止 Context Rot。
4. **術語參照 `00-AgentOS/GLOSSARY.md`**：已定義專有名詞不重複贅述。
