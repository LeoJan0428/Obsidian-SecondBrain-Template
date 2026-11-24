---
name: handoff
description: 整理並壓縮對話上下文，執行知識升遷、50/60 行雙上限校驗與 CONTEXT.md 更新，完成 Session 交接。
---

# Skill: handoff

## 目的
防止 Agent 長對話因 Context Rot 而退化，並確保有價值的工程踩坑經驗在修剪 `CONTEXT.md` 前完成升遷與固化，而非被直接抹除。

## 執行步驟 (SOP)
1. **確認目標專案與變更驗證**：
   - 確認目標專案的本地驗證指令（優先讀取當前專案根目錄 `./AGENTS.md`；舊版解耦專案則讀 `01-Projects/_active/<Project>/AGENTS.md`）已通過且 Exit Code 為 `0`。
   - 檢查當前專案 Repo 的 `git status`（僅在採用舊版解耦架構時同步檢查 Vault 的 `01-Projects/_active/<Project>/`），確認無遺漏未提交的關鍵變更。
2. **知識升遷與規則固化 (Promotion & Solidification)**：
   - **升遷至專案 `./AGENTS.md`**：若本次踩到永久性 API 邊界、資源洩漏或架構禁忌，提煉為 1–2 行 `MUST`/`NEVER` 條款插入 `[PROMOTION-ANCHOR]` 上方。
   - **觸頂固化**：若專案 `./AGENTS.md` 逼近或超過 **50 行**，必須將可自動化檢查的文字條款轉化為 Linter、型別約束或單元測試斷言，再精簡合併舊條文。
   - **升遷至 `./SPEC.md` / Vault `02-Areas/`**：若敲定了資料結構、狀態機或演算法定案，同步至專案 `./SPEC.md`；若發現跨專案共通的架構雷點或邊界教訓，提示並回寫至知識庫 `02-Areas/Software-Architecture/` 對應模式卡（維持 $\le 100$ 行）或相關領域筆記。
3. **更新並修剪 `./CONTEXT.md` ($\le 60$ 行硬上限)**：
   - 更新 `./CONTEXT.md`（舊版專案則為 `01-Projects/_active/<Project>/CONTEXT.md`）Frontmatter 的 `last_updated`。
   - 將本次完成事項加入「最近完成事項 (Recent Done)」，**嚴格只保留最近 3 筆**，更早項目於完成第 2 步升遷後移出（交由 Git Log 封存）。
   - 更新 `## 🚀 即刻下一步行動 (Immediate Next Action)` 為 1–3 項具體可執行動作。
   - 核對最終行數：專案 `./AGENTS.md` $\le 50$ 行、`./CONTEXT.md` $\le 60$ 行。
4. **跨機一致性檢查**：
   - 若本次對話新增/修改了 Skill 或全域工具依賴，強制同步更新根目錄 `README.md` 技能清冊。
5. **交接提示**：
   - 輸出簡明交接摘要（已提交 SHA、升級規則、下一步），並建議使用者開啟新 Session 接續開發。
