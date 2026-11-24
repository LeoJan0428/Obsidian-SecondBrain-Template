---
name: to-spec
description: 將釐清的需求整理輸出為標準專案規格文件 (SPEC.md)，並同步冷啟動專案領域法典 (AGENTS.md) 與工作暫存器 (CONTEXT.md)。
---

# Skill: to-spec

## 目的
將 `grill-with-docs` 釐清後的設計決策收斂為單一權威技術規格書（`SPEC.md`），並在技術棧敲定的同一瞬間完成專案 `AGENTS.md` 冷啟動，避免規格與護欄脫節。

## 執行步驟 (SOP)
1. **確認前序共識**：讀取本次對話或 `grill-with-docs` 收斂結果，以及匹配的 `02-Areas/Software-Architecture/` 模式卡與相關既有資產。
2. **建立/更新 `SPEC.md`**（預設建立於當前專案根目錄 `./SPEC.md`；若屬舊版解耦專案則更新 `01-Projects/_active/<Project>/SPEC.md`）：
   - 參考 `05-Templates/Project_Template.md` 撰寫：
     - 專案目標、範圍與非目標（Non-Goals）
     - **系統架構與模組單向依賴邊界**：明列採用的架構模式卡；若有刻意偏離模式卡的設計取捨，依 `05-Templates/Decision_Template.md` 補充簡短 ADR（背景、決策、代價）
     - 核心資料結構（DTO / Schema）、狀態機與 API 介面
     - 數學公式 / 核心演算法與非功能性需求（效能、安全、資源上限）
3. **Phase 1 冷啟動專案 `AGENTS.md` ($\le 50$ 行)**：
   - 若當前專案根目錄 `./AGENTS.md`（或舊版 `01-Projects/_active/<Project>/AGENTS.md`）尚為空殼，依 `05-Templates/Project_AGENTS_Template.md` 填入：
     - `repo_path`（當前專案根目錄，選填）
     - Section 1：技術棧、從模式卡落地的模組單向依賴邊界與資料隔離路徑
     - Section 2：僅填 2–3 條已確定的物理/技術棧硬約束與關鍵反模式防呆（**嚴禁**為了填滿格子而編造「寫乾淨代碼 / 遵守 PEP8」等空洞條文）
     - Section 3：L1 與 L2/L3 本地確定性驗證指令
4. **同步初始化 `CONTEXT.md`**：
   - 於當前專案根目錄建立 `./CONTEXT.md`（$\le 60$ 行），並指明下一步進入 `/to-tickets`（無須建立 `.code-workspace`）。
   - 若該專案預計設為 **Public** GitHub 倉儲，提醒或協助將 `CONTEXT.md`、`TICKETS.md` 等私人工作檔列入 `.gitignore`。
