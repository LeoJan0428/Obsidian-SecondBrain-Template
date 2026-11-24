---
name: dep-clean
description: 專案依賴庫瘦身、幽靈套件排查與依賴清冊校準技能 (Dependency Pruning & Requirements Hygiene)。
---

# Skill: dep-clean

## 目的
維護專案套件依賴清單之純粹度與完整性。消除未使用的肥大依賴，並強制顯式宣告代碼直接調用的套件，杜絕跨機器部署時的缺包錯誤。

## 核心原則 (Core Principles)
1. **逆向引用掃描 (Reverse Import Scan)**：
   - 依技術棧使用對應工具掃描實際引用與宣告清單之落差：Python 執行 `deptry .`（比對 `requirements.txt` / `pyproject.toml`）；JS/TS 執行 `npx knip` 或 `npx depcheck`（比對 `package.json`）。
2. **傳遞依賴顯式宣告 (Explicit Direct Dependencies)**：
   - 嚴禁依賴第三方套件夾帶安裝之隱形傳遞依賴；凡原始碼直接 `import` 之套件必須顯式列入依賴清冊。
3. **無用依賴掃除 (Prune Unused Dependencies)**：
   - 針對未曾被任何模組調用之套件，確認非 CLI/Plugin 必要工具後自清單除名。
4. **區分執行期與開發期依賴 (Runtime vs Dev Tooling)**：
   - 明確區分 Runtime 套件與本地品質／測試工具（如 `pytest`、`ruff`、`eslint`、`typescript`）。

## 執行流程
1. **依賴逆向體檢**：於專案根目錄執行技術棧對應掃描指令（`deptry .` 或 `knip` / `depcheck`）。
2. **缺漏與多餘比對**：整理「漏宣告的直接引用」與「已宣告卻未使用的套件」。
3. **校準依賴清單**：補齊缺失套件並移除廢棄項目，維持清單精準。
4. **乾淨環境驗證**：執行專案完整測試或編譯指令確認 Exit Code `0`。
5. **規範化提交**：變更封裝為 `chore(deps): ...` 提交。
