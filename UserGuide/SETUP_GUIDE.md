# 🛠️ Obsidian 筆記庫開箱與外掛設定手冊 (SETUP_GUIDE.md)

> [!IMPORTANT]
> **環境配置與 Windows 傳送門安裝步驟已統一收斂至根目錄 [SETUP.md](../SETUP.md)**。  
> 本文件專注於 **Obsidian 桌面端 GUI 設定、推薦外掛配置與常見疑難排解**。

---

## 📋 開箱檢查清單 (Quick Checklist)

- [ ] **1. 安裝核心軟體**：Obsidian (v1.5+)、Git、Python 3.10+、GitHub CLI (`gh`) 與 AI 編輯器（Antigravity / Cursor / Claude Code / Aider）。
- [ ] **2. 執行一鍵全域綁定**：依 [SETUP.md](../SETUP.md) 執行 `setup_skills_junctions.bat`，完成全域 Git Hooks、14 大技能 Junction 與憲法 HardLink。
- [ ] **3. 正確開啟 Vault**：在 Obsidian 選取 `<WORKSPACE_ROOT>\Obsidian-SecondBrain-Template\`（**切勿**選取外層 `project\` 目錄）。
- [ ] **4. 確認視力遮罩與外掛**：確認 `.obsidian/app.json` 排除規則已生效並啟用 Dataview。

---

## ⚙️ Obsidian 核心設定

### 1. 視力遮罩 (Excluded Files)
本庫已於 [.obsidian/app.json](../.obsidian/app.json) 預先版控以下排除規則，避免快取與大檔拖慢索引：
* `**/.gradle/**`、`**/.idea/**`、`**/.kotlin/**`、`**/__pycache__/**`、`**/.pytest_cache/**`、`**/.venv/**`、`**/node_modules/**`
* `**/*.pcd`、`**/*.rdk`、`**/build/**`、`**/reports/**`、`**/data/**`、`*.parquet`、`*.pkl`、`*.npy`

### 2. 內部連結與附件設定
在 Obsidian **設定 (Settings) $\rightarrow$ 檔案與連結 (Files and links)** 確認：
* **新附件預設存放路徑**：`03-Resources/attachments`（已在 `app.json` 預設）
* **內部連結類型**：建議 `最簡路徑 (Shortest path when possible)`
* **自動更新內部連結**：務必 **開啟 (ON)**

---

## 🧩 推薦 Obsidian 社群外掛 (Community Plugins)

| 外掛名稱 (Plugin) | 用途與配置建議 |
| :--- | :--- |
| **Dataview** *(建議安裝)* | 驅動 [DASHBOARD.md](../DASHBOARD.md) 動態表格；安裝後務必於設定開啟 **Enable JavaScript Queries**。 |
| **Canvas** *(內建核心外掛)* | 預設啟用，可直接開啟 [PROJECTS_WAR_ROOM.canvas](../PROJECTS_WAR_ROOM.canvas)。 |
| **Obsidian Web Clipper** *(瀏覽器擴充)* | 目標資料夾設為 `_inbox`，範本貼入 [WebClipper_Template.md](../05-Templates/WebClipper_Template.md)。 |
| **Templater** *(選配)* | 若使用模板插入筆記，將範本資料夾設為 `05-Templates/`。 |
| **Smart Connections** *(選配)* | 本地語意搜尋側邊欄；建議在設定中排除 `04-Archive`。 |

---

## 🩺 疑難排解 (Troubleshooting)

### Q1：換新電腦或獨立 Repo 讀不到全域技能或規範？
* **解法**：於本知識庫根目錄重新執行 [`setup_skills_junctions.bat`](../setup_skills_junctions.bat)，並依 [SETUP.md](../SETUP.md) 的 PowerShell 驗證指令確認 `core.hooksPath`、`~/.gemini/config/AGENTS.md` 與 14 個技能目錄皆生效。

### Q2：終端 `git commit` 遭到拒絕？
* **解法**：依 [00-AgentOS/hooks/](../00-AgentOS/hooks/) 提示處理：
  * `pre-commit` 攔截：代表暫存區含機密檔、金鑰樣式、`__pycache__` 或 $>500\text{KB}$ 檔案，執行 `git reset HEAD -- "<檔案>"` 移出暫存後修正。
  * `commit-msg` 攔截：確認第一行符合 `<type>(<scope>): <subject>` 格式（允許 `feat|fix|docs|refactor|chore|test|ci|build|perf|style|revert`）。

### Q3：如何新增或修改 Skill？
* **解法**：直接編輯 `00-AgentOS/skills/<skill-name>/SKILL.md`，Windows Junction 會零延遲同步至 `.agents`、`.claude`、`.cursor` 與 `~/.gemini/config/skills`；異動技能時務必同步更新根目錄 [README.md](../README.md) 技能清冊。
