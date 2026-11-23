# 🛠️ SecondBrain Obsidian 與環境開箱清單 (SETUP.md)

> AI Agent 跨機初始化指令與 14 大技能清冊請以根目錄 [README.md](./README.md) 為準；詳細圖文排錯請參閱 [UserGuide/SETUP_GUIDE.md](./UserGuide/SETUP_GUIDE.md)。

---

## ⚡ Obsidian 端 4 步設定

1. **開啟正確 Vault 根目錄**：
   - 務必開啟 `<WORKSPACE_ROOT>\Obsidian-SecondBrain-Template\`（你的 Vault 資料夾），**切勿**開啟更外層目錄。
2. **確認檔案排除與附件存放路徑**（已同步版控於 `.obsidian/app.json`）：
   - `attachmentFolderPath`：`03-Resources/attachments`（防止貼圖散落根目錄）。
   - `userIgnoreFilters`：已排除 `**/data/**`、`**/reports/**`、`**/.venv/**`、`**/node_modules/**` 等雜訊路徑。
3. **啟用必備外掛**：
   - **Dataview**（社群外掛）：安裝啟用後，務必於設定中開啟 **Enable JavaScript Queries** 與 **Enable Inline JavaScript Queries**，即可驅動 [DASHBOARD.md](./DASHBOARD.md)。
   - **Canvas**（內建核心外掛）：已預設啟用，可直接開啟 [PROJECTS_WAR_ROOM.canvas](./PROJECTS_WAR_ROOM.canvas)。
   - **Obsidian Web Clipper**（瀏覽器擴充，可選）：目標資料夾設為 `_inbox`，範本貼入 [05-Templates/WebClipper_Template.md](./05-Templates/WebClipper_Template.md)。
4. **開發專案開啟方式（Code-Vault 解耦）**：
   - 所有專案程式碼獨立位於 `<WORKSPACE_ROOT>\repos\<專案>\`。
   - 寫程式時直接打開 `<WORKSPACE_ROOT>\workspaces\<專案>.code-workspace`，即可在單一編輯器視窗內同時存取程式碼、全域憲法與專案治理四件套。
