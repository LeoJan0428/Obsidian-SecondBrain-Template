---
name: dep-clean
description: 專案依賴庫瘦身、幽靈套件排查與 requirements.txt 自動校準技能 (Dependency Pruning & Requirements Hygiene)。
---

# Skill: dep-clean

## 目的
維護專案套件依賴清單之純粹度與完整性。消除未使用的多餘肥大依賴，並強制將代碼中直接調用的套件（如 `requests`）明確顯式宣告，杜絕跨機器部屬時的 `ModuleNotFoundError`。

## 核心原則 (Core Principles)
1. **逆向引用掃描 (Reverse Import Scan via deptry)**：
   - 執行 `deptry .` 掃描專案所有 `.py` 檔案，精確比對 `requirements.txt` 與代碼實際 `import` 樹。
2. **傳遞依賴顯式宣告 (Explicit Direct Dependencies)**：
   - 嚴禁依賴第三方套件夾帶安裝之隱形依賴（Transitive Dependencies）。只要代碼中有 `import requests` 或 `import urllib3`，必須直接登記於 `requirements.txt`。
3. **無用依賴掃除 (Prune Unused Dependencies)**：
   - 針對未曾被任何模組調用的套件，評估後自依賴清冊除名，縮減 Docker 映像檔與伺服器記憶體佔用。
4. **開發工具依賴標註 (Dev/Test Tooling Annotation)**：
   - 清楚區分核心執行期套件（Runtime）與本地品質測試工具（`pytest`, `pytest-archon`, `ruff`）。

## 執行流程
1. **依賴逆向體檢**：
   - 於專案目錄執行 `deptry .`。
2. **缺漏與多餘比對**：
   - 整理「漏宣告的直接引用 (DEP003)」與「定義了卻沒用到的套件 (DEP002)」。
3. **校準 requirements.txt**：
   - 補齊缺失套件並移除廢棄項目，保持依賴清單 100% 精準。
4. **乾淨環境驗證**：
   - 執行核心測試確認無套件缺失報錯。
5. **規範化提交**：
   - 變更封裝為 `chore(deps): ...` 提交。

