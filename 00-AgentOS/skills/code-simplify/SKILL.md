---
name: code-simplify
description: 專案代碼簡化、死代碼掃除與架構抗腐化技能 (Code Simplification & Clean Architecture Hygiene)。
---

# Skill: code-simplify

## 目的
在不改變既有系統行為的前提下，消除死代碼、清理無用引用、降低複雜度並拆解過長上帝物件，保持專案長期健壯與可讀性。

## 核心原則 (Five Pillars)
1. **行為絕對不變性 (Behavior Preservation)**：簡化前必須有測試或靜態檢查基準；簡化後所有驗證必須 100% 通過，嚴禁破壞外部接口或業務副作用。
2. **靜態工具第一防線 (Tool-Assisted First)**：
   - 依技術棧啟用對應 Linter/型別工具掃除未用 Import 與死變數（如 Python 用 `ruff check --select F821,F401,F841 --fix`，TS/JS 用 `eslint` / `tsc --noEmit`）。
   - 杜絕盲目例外吞噬（空 `except: pass` 或空 `catch {}`），替換為精準例外處理或明確 Log。
3. **上帝物件拆解 (Decompose God Objects)**：
   - 當單一模組長度接近或超過 600 行時，依職責將格式化、渲染或輔助函式抽離至獨立子模組。
4. **嚴格作用域鎖定 (Scope Lockdown)**：
   - 嚴禁盲猜刪除「看似沒用」但外部依賴的代碼；清理前須先掃描全局引用關係。
5. **獨立原子提交 (Atomic Commits)**：
   - 清理與簡化操作一律單獨封裝為 `refactor:` 或 `chore:` 提交，嚴禁與 `feat:` 混合。

## 執行流程
1. **預檢與基準對齊**：執行專案 `AGENTS.md` 指定的測試或型別驗證指令，確保清理前為綠燈。
2. **自動化工具掃除**：執行技術棧對應的 Linter 清理語法雜訊與無用引用。
3. **架構邊界檢查**：若專案設有架構邊界測試（如 `pytest-archon` 或模組依賴規則），確認領域層純粹度無退化。
4. **複雜度精簡**：減少深層巢狀、改用提早 `return` 與資料驅動查表。
5. **後驗與原子提交**：重跑完整驗證確認 Exit Code `0`，依 Conventional Commits 提交。
