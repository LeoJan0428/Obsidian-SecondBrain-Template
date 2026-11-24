---
name: code-review
description: 對變更進行標準與規格面雙軸度的審查。
---

# Skill: code-review

## 目的
從工程品質與需求規格雙軸度把關程式碼變更，於提交或開 PR 前攔截回歸與架構退化。

## 執行步驟
1. **規格面審查 (Spec & Invariants Axis)**：
   - 檢視 `git diff` 是否嚴格對齊 `./SPEC.md`、`./TICKETS.md` 驗收條件及專案 `./AGENTS.md` 之 `MUST`/`NEVER` 領域不變量，無作用域外擅改。
2. **標準面審查 (Engineering & Security Axis)**：
   - 檢查靜態檢查/型別通過狀態、邊界與異常處理（禁盲目 `except: pass`）、資源生命週期釋放、檔案讀寫編碼及潛在密鑰/注入風險。
3. **輸出審查裁決**：依嚴重度列出具體檔名與行號問題，確認驗證指令 Exit Code `0`。
