---
name: code-simplify
description: 專案代碼簡化、死代碼掃除與架構抗腐化技能 (Code Simplification & Clean Architecture Hygiene)。
---

# Skill: code-simplify

## 目的
在不改變既有系統行為的前提下，消除死代碼、清理無用引用、降低圈複雜度並拆解千行上帝物件，保持專案長期健壯與可讀性。

## 核心原則 (Five Pillars)
1. **行為絕對不變性 (Behavior Preservation)**：簡化前必須有測試覆蓋；簡化後所有測試必須 100% 通過，嚴禁破壞外部接口、回傳格式或業務副作用。
2. **靜態工具第一防線 (Tool-Assisted First)**：
   - 執行 `ruff check --select F821,F401,F841 --fix` 掃除未宣告引用、未用 Import 與死變數。
   - 杜絕盲目例外吞噬 (`except Exception: pass`)，替換為精準例外捕獲或明確 Log。
3. **上帝物件拆解 (Decompose God Objects)**：
   - 當單一模組長度接近或超過 600 行時，依職責將非核心的字串渲染、數據格式化或輔助工具函數抽離至獨立子模組。
4. **嚴格作用域鎖定 (Scope Lockdown)**：
   - 嚴禁盲猜或無授權刪除「看似沒用」但外部依賴的代碼；清理前須先掃描全局引用關係。
5. **獨立原子提交 (Atomic Commits)**：
   - 清理與簡化操作一律單獨封裝為 `refactor:` 或 `chore:` 提交，嚴禁與業務功能 (`feat:`) 混合。

## 執行流程
1. **預檢與基準對齊 (Baseline Check)**：
   - 執行專案本地測試（如 `pytest tests/ -q`），確保清理前為純綠燈基準。
2. **自動化工具掃除 (Automated Hygiene)**：
   - 執行 `ruff` 清理語法雜訊與無用 Import。
3. **架構邊界檢查 (Boundary Audit)**：
   - 執行 `pytest-archon` 驗證領域層純粹度，確認無向後相容 Facade 或孤立殘留檔案。
4. **複雜度精簡 (Complexity Reduction)**：
   - 減少巢狀 `if-else`、提早 `return`、簡化多餘的中間變數。
5. **後驗與原子提交 (Post-Verification & Commit)**：
   - 再次執行完整測試套件。
   - 遵循 Conventional Commits 規範化提交。

