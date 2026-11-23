# 🛠️ SecondBrain 開箱建置完整教學 (SETUP.md)

> 14 大全域技能清冊請參閱根目錄 [README.md](./README.md)；進階使用手冊與元件說明請參閱 [UserGuide/SETUP_GUIDE.md](./UserGuide/SETUP_GUIDE.md)。

---

## 步驟 1：從 GitHub Template 建立並下載本機

1. 在 GitHub 範本頁右上角點擊綠色 **Use this template → Create a new repository**（建議將自己的個人知識庫設為 **Private**）。
2. Clone 到本機工作目錄（建議與程式碼倉儲同層）：
   ```powershell
   mkdir <WORKSPACE_ROOT>\repos
   cd <WORKSPACE_ROOT>
   git clone https://github.com/<YOUR_USERNAME>/<YOUR_VAULT_REPO>.git
   ```

---

## 步驟 2：一鍵配置全域規則、14 大技能與 Git 金鑰防線

在檔案總管雙擊根目錄下的 **`setup_skills_junctions.bat`**，或在終端機執行：

```cmd
cd <WORKSPACE_ROOT>\<YOUR_VAULT_REPO>
.\setup_skills_junctions.bat
```

這支腳本會自動完成 4 項全域綁定（換新電腦或重灌時只需執行這一次）：
1. **全域與本地 Git Hooks（防金鑰外洩）**：設定 `core.hooksPath` 至 `00-AgentOS/hooks`（攔截 `.env`、`local.properties`、`*.pem`/`*.key`、API Key / 私鑰樣式與超過 500KB 檔案），並啟用 UTF-8 中文路徑與 LF 換行規範。
2. **本機工作區技能傳送門**：以 NTFS Junction 將 `00-AgentOS/skills/` 映射至 `.agents\skills`、`.claude\skills` 與 `.cursor\skills`。
3. **Antigravity 機器全域技能**：建立 `%USERPROFILE%\.gemini\config\skills` $\to$ `00-AgentOS\skills`。
4. **Antigravity 機器全域憲法**：同步 `%USERPROFILE%\.gemini\config\AGENTS.md` $\to$ 根目錄 `AGENTS.md`。

### 驗證設定是否生效（PowerShell）
```powershell
git config --global --get core.hooksPath
Test-Path "$env:USERPROFILE\.gemini\config\AGENTS.md"
(Get-ChildItem "$env:USERPROFILE\.gemini\config\skills" -Directory).Count
```
預期依序回傳：`.../00-AgentOS/hooks`、`True`、`14`。

---

## 步驟 3：Obsidian 端設定

1. **開啟正確 Vault 根目錄**：
   * 在 Obsidian 選擇 **Open folder as vault**，務必選取 `<WORKSPACE_ROOT>\<YOUR_VAULT_REPO>\`，**切勿**選取更外層目錄。
2. **附件與檔案排除規則**（已預先版控於 `.obsidian/app.json`）：
   * `attachmentFolderPath`：`03-Resources/attachments`（避免貼圖散落根目錄）。
   * `userIgnoreFilters`：已排除 `**/data/**`、`**/reports/**`、`**/.venv/**`、`**/node_modules/**` 等快取雜訊。
3. **啟用建議外掛**：
   * **Dataview** *(社群外掛，選配)*：若需使用 [DASHBOARD.md](./DASHBOARD.md)，安裝後開啟 **Enable JavaScript Queries** 與 **Enable Inline JavaScript Queries**。
   * **Canvas** *(內建核心外掛)*：已預設啟用，可直接開啟 [PROJECTS_WAR_ROOM.canvas](./PROJECTS_WAR_ROOM.canvas)。
   * **Obsidian Web Clipper** *(瀏覽器擴充，選配)*：目標資料夾設為 `_inbox`，範本可貼入 [05-Templates/WebClipper_Template.md](./05-Templates/WebClipper_Template.md)。

---

## 步驟 4：開始新專案與啟用自動 PR/CI 閉環

採 **單倉自包含模式**，日常寫程式不再需要 `.code-workspace`：

1. **建立並開啟專案**：
   * 在 `<WORKSPACE_ROOT>\repos\<專案>\` 初始化獨立 Git 倉儲（IDE、桌面 App 或 `agy` CLI 直接開啟此資料夾即可自動載入全域規則與 14 大技能）。
   * 將該專案的 `AGENTS.md`（$\le 50$ 行）、`CONTEXT.md`（$\le 60$ 行）、`SPEC.md`、`TICKETS.md` 直接放在專案根目錄。
   * 若該倉儲預計設為 **Public**，請將 `CONTEXT.md`、`TICKETS.md` 等私人工作檔列入該專案的 `.gitignore`。
2. **啟用自動分支與 GitHub PR/CI 閉環（建議）**：
   * 安裝 GitHub CLI 並登入（每台電腦只需一次）：
     ```powershell
     winget install --id GitHub.cli -e --accept-package-agreements --accept-source-agreements
     gh auth login
     ```
   * 在目標專案新增 `.github/workflows/ci.yml`（例如 Lint、Unit Test 與 Gitleaks Secret Scan）。
   * 當專案同時綁定 GitHub Remote 且具備 `.github/workflows/ci.yml` 時，Agent 進行 L2/L3 開發會自動於主線外開功能分支、本機驗證後推送開 PR 並監看 CI 直到全綠燈，最後交由人類審核合併（**絕不自動 Merge**）。
3. **建議於 GitHub 網頁開啟 Push Protection**：
   * 至 GitHub 網頁右上角頭像 → **Settings → Code security** 開啟 **Push protection**，即使新建尚未建立 `.yml` 的倉儲也能在 `git push` 瞬間擋下意外金鑰。
