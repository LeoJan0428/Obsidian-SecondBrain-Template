# 🏗️ Area: Software Architecture Playbooks (系統架構模式庫)

本區收錄跨專案高穩定度的**架構邊界模式卡**，用於新專案啟動前防呆與反模式避坑；單一專案的技術選型與取捨（為什麼選 A 不選 B）請使用 [[05-Templates/Decision_Template]] 記錄在各專案 Repo 內，避免將框架死範本照搬為「貨物崇拜（Cargo-Cult）」。

所有模式卡嚴格控制於 **$\le 100$ 行**，並遵循 [[00-AgentOS/PROFILE]] 的 `GLOBAL-01`（Explore $\to$ Expand 3X 演進）。

---

## 🧭 專案題型 $\to$ 模式卡快速路由表

| 專案題型 / 特徵 | 對應模式卡 | 核心防呆目標 |
| :--- | :--- | :--- |
| LLM 互動、Agent、遊戲 NPC、工具呼叫 | [01. Hybrid LLM 互動應用 / Agent / 遊戲 NPC](./01_hybrid_llm_app_and_npc.md) | 確定性規則核心與 LLM 敘事分離、防幻覺與低延遲 |
| FastAPI / REST / RPC 後端服務 | [02. Python 後端 API 服務](./02_python_api_service.md) | 路由、用例、領域邏輯、外部 I/O 單向依賴邊界 |
| React / React Native (Expo) 互動前端 | [03. 前端 / 手機 App 應用](./03_mobile_web_client_app.md) | 伺服器快取與本地 UI 狀態分離、Feature Colocation |
| 量化回測、模型訓練、數據處理管線 | [04. 資料分析 / ML 實驗管線](./04_data_ml_pipeline.md) | 防資料洩漏、時間序切分、原始資料不可變與可重現 |

---

## 🔄 與 AgentOS 工作流的複利閉環
1. **開案檢視**：執行 `grill-with-docs` 時先對照上表，命中題型即載入對應模式卡的反模式警告與必問清單。
2. **規格落地**：執行 `to-spec` 時將採用的邊界寫入專案 `SPEC.md` 與 `AGENTS.md`（若有意偏離模式卡，須附帶 ADR 說明）。
3. **實戰回寫**：執行 `handoff` 時若踩到跨專案共通雷點，將精簡教訓回寫至對應模式卡的「高頻反模式」區塊。
4. **新增模式卡**：使用 [[05-Templates/Architecture_Playbook_Template]] 建立新卡，並同步登記至上方路由表。
