---
name: doc-cleanup
description: 知識庫文檔抗腐化、歷史研報歸檔與 Markdown 一致性稽核技能 (Documentation Pruning & Context Rot Defense)。
---

# Skill: doc-cleanup

## 目的
防止 SecondBrain 知識庫因長期運行累積過期研報、草稿與舊規格而產生「上下文腐化 (Context Rot)」，確保 AI 檢索時永遠讀取最真實、最精簡之第一手資訊。

## 核心原則 (Core Principles)
1. **研報階梯歸檔 (Tiered Report Archiving)**：
   - 專案 `reports/` 下超過 14 天之過期生成報表，主動引導打包遷移至 `04-Archive/` 或子專案 `reports/archive/`，維護當前工作區整潔。
2. **50/60 行雙滾動窗口守護 (Dual Rolling Window)**：
   - 嚴格稽核專案 `AGENTS.md` ($\le 50$ 行) 與 `CONTEXT.md` ($\le 60$ 行)。
   - 確保 `CONTEXT.md` 之「最近完成事項」永遠只保留最近 3 筆，歷史進度交由 Git Log 封存。
3. **文檔與代碼一致性校驗 (Code-Doc Synchronization)**：
   - 檢查 `README.md`、`SPEC.md` 與註解中的檔案路徑（如重構後的 `src/domain`），杜絕已刪除舊路徑繼續殘留於文檔。
4. **排除暫存污物與未追蹤快照 (Artifact Sanitization)**：
   - 檢查是否有日報生成的臨時 JSON 或過大檔案未被 `.gitignore` 排除，保持 Git Status 清爽。

## 執行流程
1. **盤點掃描**：
   - 搜尋專案內所有 Markdown 研報與暫存檔，按修改時間排序。
2. **過期分流**：
   - 將超過 14 天之歷史日報打包整理，避免污染根目錄與搜尋索引。
3. **窗口修剪**：
   - 依據全域憲法修剪 `CONTEXT.md`，將重要經驗升遷至 `AGENTS.md` / `SPEC.md`。
4. **一致性替換**：
   - 搜尋過時符號或廢棄模組名稱，修正為最新領域模型路徑。
5. **規範化提交**：
   - 變更封裝為 `docs:` 提交。

