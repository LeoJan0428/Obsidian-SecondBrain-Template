# 🛠️ SecondBrain 開箱安裝與環境設定手冊 (SETUP_GUIDE.md)

> [!IMPORTANT]
> **新電腦或新工作區開箱必讀**  
> 本文件列出在使用本知識庫進行開發、寫筆記與多代理 AI 協同工作前，**所有必須安裝的軟體、Windows 傳送門配置、Obsidian 關鍵設定與外掛推薦清單**。照著打勾執行即可完成 100% 開箱準備。

---

## 📋 快速開箱檢查清單 (Quick Checklist)

- [ ] **1. 核心軟體安裝**：Obsidian、Git、Python 3.10+、AI 編輯器（Antigravity / Cursor / Claude Code / Aider）。
- [ ] **2. 執行環境與傳送門一鍵配置**：雙擊根目錄下的 `setup_skills_junctions.bat`（1 秒完成）。
- [ ] **3. 正確開啟 Obsidian**：確認開啟的目錄是本知識庫根目錄（`<WORKSPACE_ROOT>\Obsidian-SecondBrain-Template`）。
- [ ] **4. 配置視力遮罩 (Excluded Files)**：在 Obsidian 中屏蔽快取與二進位檔案。
- [ ] **5. 安裝 Obsidian 社群外掛**：安裝 Dataview（必裝）、Smart Connections（可選）。
- [ ] **6. 驗證 Git 雙守門機制**：確認 `pre-commit` 與 `commit-msg` 正常運作。

---

## 💻 第一步：核心軟體與執行環境安裝

### 1. 筆記與開發核心工具
1. **Obsidian (筆記大腦)**：
   * 下載官網：[https://obsidian.md/](https://obsidian.md/)
   * 建議版本：v1.5.0 以上（支援最新 Properties 屬性檢視）。
2. **Git (版本控制)**：
   * 下載官網：[https://git-scm.com/](https://git-scm.com/)
   * 確認終端可用：`git --version`
3. **Python (量化與自動化執行環境)**：
   * 建議版本：**Python 3.10 ~ 3.11**（與科學計算庫相容性最佳）。
   * 確認終端可用：`python --version` 或 `py --version`。

### 2. 多代理 AI 編輯器（可任意切換或搭配使用）
* **Google Antigravity (原生推薦)**：原生讀取 `AGENTS.md` 與 `.agents/skills/`，無須額外指針檔。
* **Cursor**：原生讀取根目錄 `AGENTS.md` 與 `.cursor/skills/`。
* **Claude Code**：讀取根目錄 `CLAUDE.md`（內含 `@AGENTS.md`）與 `.claude/skills/`。
* **Aider**：讀取根目錄 `.aider.conf.yml`（自動加載 `AGENTS.md`）。

---

## ⚡ 第二步：Windows 環境與技能傳送門一鍵建立

本知識庫將工程技能實體唯一保存在 [00-AgentOS/skills/](../00-AgentOS/skills/)，讓你在 Obsidian 中能隨時打開檢視與修改。

### 操作步驟（只需 1 秒）：
1. 在檔案總管中，進到本知識庫根目錄。
2. **對著 [`setup_skills_junctions.bat`](../setup_skills_junctions.bat) 滑鼠點兩下執行**！
3. 批次檔會全自動完成兩大核心工程設定：
   * **Git 核心配置升級**：
     * `git config core.hooksPath 00-AgentOS/hooks`（將 Git Hooks 綁定至版本控管目錄）
     * `git config core.quotepath false`（解決 Windows 中文路徑轉義導致 Hook 失效的問題）
     * `git config core.autocrlf input`（防止 Windows CRLF 破壞 Shell 腳本執行）
   * **NTFS Junction 目錄傳送門**：
     * `.agents\skills` $\longleftrightarrow$ `00-AgentOS\skills`
     * `.claude\skills` $\longleftrightarrow$ `00-AgentOS\skills`
     * `.cursor\skills` $\longleftrightarrow$ `00-AgentOS\skills`

---

## ⚙️ 第三步：Obsidian 筆記庫核心關鍵設定

打開 Obsidian，點擊 **「開啟現有資料夾作為筆記庫 (Open folder as vault)」**：
> ⚠️ **重要防呆**：請務必選取 `<WORKSPACE_ROOT>\Obsidian-SecondBrain-Template`（本知識庫根目錄）資料夾，**千萬不要選到更外層的工作區目錄**！

### 1. 關鍵設定：物理視力遮罩 (Excluded Files)
確保 Obsidian 打開飛快、不被快取與二進位檔卡死：
1. 打開 Obsidian $\rightarrow$ 左下角 **設定 (Settings)** $\rightarrow$ **檔案與連結 (Files and links)**。
2. 找到 **已排除的檔案 (Excluded files)**，確認包含以下規則（本庫已在 `.obsidian/app.json` 預設配好）：
   ```text
   **/.gradle/**
   **/.idea/**
   **/.kotlin/**
   **/__pycache__/**
   **/.pytest_cache/**
   **/.venv/**
   **/node_modules/**
   **/*.pcd
   **/*.rdk
   **/build/**
   **/reports/**
   ```

### 2. 內部連結與附件設定
* **設定 $\rightarrow$ 檔案與連結**：
  * **內部連結類型**：建議選擇 `最簡路徑 (Shortest path when possible)`。
  * **自動更新內部連結**：務必 **開啟 (ON)**，移動筆記時所有 `[[Link]]` 自動更新。

---

## 🧩 第四步：推薦 Obsidian 社群外掛 (Community Plugins)

打開 Obsidian 設定 $\rightarrow$ **社群外掛 (Community plugins)** $\rightarrow$ 關閉安全模式 $\rightarrow$ 點擊 **瀏覽 (Browse)** 安裝：

| 外掛名稱 (Plugin) | 推薦理由 | 安裝後的建議配置 |
| :--- | :--- | :--- |
| **Dataview** *(必裝)* | 讓筆記庫具備資料庫查詢能力。自動生成專案進度清單與 MOC。 | 安裝後開啟 `Enable JavaScript Queries`。 |
| **Smart Connections** *(可選)* | 本地向量語意搜尋。在側邊欄即時呈現與當前筆記最相關的知識卡片。 | 需填入 API Key 或連線本地 Ollama；設定中排除 `01-Projects`。不裝亦不影響全庫 AI 功能。 |
| **Templater** *(推薦)* | 強化範本渲染引擎。在新建筆記時自動填入日期、標題與關聯檔案。 | 將範本資料夾設為 `05-Templates/`。 |
| **Paste URL into Selection** | 複製網址後反白文字按下 `Ctrl+V`，自動轉為 Markdown 超連結格式。 | 預設即可。 |

---

## 🛡️ 第五步：驗證 Git 本地雙守門機制 (Hooks)

本庫透過 `00-AgentOS/hooks/` 提供兩層自動防護：

1. **`pre-commit`（安全守門）**：
   * 提交前自動攔截 `.env`、`__pycache__`、`workspace.json` 或 `scratch/`。
2. **`commit-msg`（格式與去水印守門）**：
   * 自動剝除 `Co-authored-by:` 等多餘標籤。
   * 強制檢驗第一行是否符合 Conventional Commits 格式（如 `feat(scope): subject`）。

---

## 🩺 疑難排解 (Troubleshooting)

### Q1：換了新電腦或重拉 Git 專案，AI 說找不到技能怎麼辦？
* **解法**：直接對著專案根目錄下的 [`setup_skills_junctions.bat`](../setup_skills_junctions.bat) 點兩下，傳送門與 Git 設置 1 秒自動搭好。

### Q2：為什麼在終端 commit 時顯示拒絕？
* **解法**：檢查報錯訊息：
  * 若為 `pre-commit` 報錯：代表你 stage 了 `.env`、`__pycache__` 或 `workspace.json`，請執行 `git reset HEAD <檔案>` 將其解除暫存。
  * 若為 `commit-msg` 報錯：代表 Commit 訊息不符合 `<type>(<scope>): <subject>` 格式（例如需寫成 `feat(agent): 新增功能`）。

### Q3：我想為知識庫修改規範或新增專屬 Skill 該怎麼做？
* **解法**：請參閱 [USER_GUIDE.md § 系統自訂與擴充指南](./USER_GUIDE.md)。直接在 `00-AgentOS/skills/` 建立資料夾與 `SKILL.md`，Windows Junction 會自動同步至所有 AI 編輯器！

