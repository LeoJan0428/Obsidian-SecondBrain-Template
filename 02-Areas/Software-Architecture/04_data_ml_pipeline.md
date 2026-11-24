---
title: "資料分析 / ML 實驗管線架構模式卡"
type: playbook
domain: "[[02-Areas/Software-Architecture/README]]"
tags: [architecture, playbook, data, ml, pipeline]
last_updated: "2026-11-24"
---

# 📊 04. 資料分析 / ML 實驗管線

## 1. 適用題型與禁用條件 (When to Use / When NOT to Use)
* **適用**：量化金融回測、機器學習訓練／推論、需要嚴格防資料洩漏（Data Leakage）與結果可重現的數據管線。
* **禁用**：一次性的探索性圖表繪製（Ad-hoc EDA，直接寫精簡分析腳本即可，切勿過度管線化）。

## 2. 核心邊界與單向依賴 (Core Boundaries & Dependency Rule)
```text
Bronze (data/raw: 唯讀原始快照，嚴禁覆寫)
  --> Silver (清洗、型別與 Schema 驗證)
  --> Gold (特徵工程與切分後訓練集)
  --> Pipeline / Model (fit 僅限 Train Split，嚴格鎖定隨機種子)
```
* **資料分層不可逆**：原始資料永遠唯讀（Append-only / Immutable），所有清洗與衍生特徵寫入下游新路徑。
* **前處理封裝（Pipeline Encapsulation）**：標準化（Scaler）、缺失值填補、編碼器一律與模型綁在同一個 Pipeline／DAG，`fit` 僅允許接觸訓練集。
* **測試資料隔離**：單元測試僅讀取 `tests/fixtures/` 下的迷你合成或脫敏樣本，禁止依賴本地大型原始檔案。

## 3. 高頻反模式與爆點 (Failure Modes & Anti-Patterns)
* ❌ **全集前處理洩漏（Data Leakage）**：先對整份資料做標準化或目標編碼再切 Train/Test，導致離線指標虛高、上線或實盤慘敗。
* ❌ **時間序列隨機切分（Lookahead Bias）**：對金融／時序資料使用 `shuffle=True` 隨機切分，讓模型偷看到未來資訊。
* ❌ **Notebook 幽靈狀態（Hidden State）**：跳格執行或直接覆寫原始檔，導致三天後再也跑不出同一組驗證分數。
* ❌ **訓練／推論特徵不一致（Offline/Online Skew）**：訓練時與即時推論時用了兩套不同邏輯算特徵，靜默產生錯誤預測。

## 4. Explore → Expand 演進門檻 (對齊 `GLOBAL-01`)
* **Explore 最小骨架**：唯讀 `data/raw` + 可重複執行的 CLI 切分/評估腳本 + 固定 Random Seed。
* **切換 Expand 紅燈**：進入長期調參、競賽繳交或上線排程時，再補入 Schema 斷言（防缺值／分佈飄移）、實驗參數追蹤與特徵一致性單元測試。

## 5. 開案必問 3–5 題 (Socratic Checklist for `grill-with-docs`)
1. **切分與防洩漏策略**：資料是否具時間序列或群組相依性？Train / Validation / Test 的切分邊界如何杜絕 Lookahead Bias？
2. **資料不可變與 Fixtures**：原始資料存哪裡、有多大？無原始檔環境（CI）要用什麼小型 Fixture 跑測試？
3. **重現性基準**：需要鎖定哪些隨機種子、套件版本、資料快照與實驗設定，才能保證「同輸入必得同結果」？
4. **指標對齊真實目標**：離線評估指標（如 RMSE / Sharpe）是否真正對應最終業務損益或交易摩擦成本？

## 6. 權威出處 (Tier 1 / Tier 2 References)
* Google Developers, *Rules of Machine Learning: Best Practices for ML Engineering*
* Databricks / Lakehouse Architecture, *Medallion Architecture (Bronze / Silver / Gold)*
* Made With ML & scikit-learn Official Docs (*Pipelines and Composite Estimators*)
