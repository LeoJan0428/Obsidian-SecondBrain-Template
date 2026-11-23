---
name: tech-debt-audit
description: 專案技術債全面體檢、架構腐化審查與例外黑洞排查技能 (Technical Debt Audit & Code Smells Assessment)。
---

# Skill: tech-debt-audit

## 目的
全面評估專案代碼庫之技術債務、架構邊界純粹度、例外處理健壯性與單檔圈複雜度，在功能崩潰前主動揪出定時炸彈。

## 核心原則 (Core Principles)
1. **上帝物件預警 (God Object Detection)**：
   - 掃描所有模組行數，單檔超過 600 行者（如 `adaptive_tuner.py`、`daily_updater.py`、`telegram_bot_service.py`）列入高圈複雜度監控名單，建議依職責拆解為正交子模組。
2. **例外吞噬阻斷 (Exception Swallowing Elimination)**：
   - 嚴格排查 `except Exception: pass`（`BLE001` / `S110`），杜絕潛在 `NameError` 或 `TypeError` 被靜音吞噬。
3. **架構分層防禦 (Layer Isolation via pytest-archon)**：
   - 驗證 Domain 核心層（如 `src.domain.*`）嚴禁反向依賴外層 Presentation、Web Controllers 或 Notifications。
4. **現代化語法與型別規範 (Modern Python Typing)**：
   - 掃描過時之 `typing.Dict` / `typing.List`，引導遷移至 Python 3.10 原生 `dict` / `list` / `| None`。
5. **優先級評分卡輸出 (Actionable Health Scorecard)**：
   - 不只列出問題，必須依危害程度（P0 致命未定義、P1 例外黑洞、P2 上帝物件、P3 語法雜訊）提供前三大改善建議。

## 執行流程
1. **靜態工具快篩**：
   - 執行 `ruff check src/ --statistics` 與 `ruff check src/ --select F821` 快速盤點錯誤分佈。
2. **架構邊界測試**：
   - 執行 `pytest tests/test_architecture_boundaries.py -q` 驗證分層隔離。
3. **複雜度與代碼長度分析**：
   - 統計 Top 10 最大檔案行數與類別方法分佈。
4. **輸出技術債綜合評估報告**：
   - 明確標註健康指標與具體重構建議路徑。

