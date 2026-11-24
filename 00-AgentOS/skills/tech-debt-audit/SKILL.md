---
name: tech-debt-audit
description: 專案技術債全面體檢、架構腐化審查與例外黑洞排查技能 (Technical Debt Audit & Code Smells Assessment)。
---

# Skill: tech-debt-audit

## 目的
全面評估專案代碼庫之技術債務、架構邊界純粹度、例外處理健壯性與單檔圈複雜度，在功能崩潰前主動揪出定時炸彈。

## 核心原則 (Core Principles)
1. **上帝物件預警 (God Object Detection)**：
   - 掃描原始碼模組行數，單檔超過 600 行者列入高複雜度監控名單，建議依單一職責拆解為正交子模組。
2. **例外吞噬阻斷 (Exception Swallowing Elimination)**：
   - 嚴格排查盲目吞噬例外（如 Python `except Exception: pass` / `S110`、JS/TS 空 `catch {}`），杜絕潛在錯誤被靜音掩蓋。
3. **架構分層防禦 (Layer Isolation)**：
   - 驗證核心領域層（Domain / Core）嚴禁反向依賴外層 Presentation、Controllers 或外部 I/O。
4. **現代化型別與語法規範 (Strict Typing Hygiene)**：
   - 檢查弱型別逃逸或過時寫法（如 Python 舊式 `typing.Dict`/`List`、TypeScript `any`）。
5. **優先級評分卡輸出 (Actionable Health Scorecard)**：
   - 依危害程度（P0 致命缺陷、P1 例外黑洞、P2 上帝物件、P3 型別/風格雜訊）提供前三大改善建議。

## 執行流程
1. **靜態工具快篩**：
   - 依專案技術棧執行對應檢查（例：Python 用 `ruff check src/ --statistics`；TS/JS 用 `npx tsc --noEmit` / `eslint`；或專案 `AGENTS.md` 指定閘門）。
2. **架構邊界測試**：
   - 執行專案既有架構邊界測試或完整測試套件（如 `pytest` / `npm test`）。
3. **複雜度與代碼長度分析**：
   - 統計 Top 10 最大檔案行數與高複雜度函式分佈。
4. **輸出技術債綜合評估報告**：
   - 明確標註健康指標與具體重構建議路徑。
