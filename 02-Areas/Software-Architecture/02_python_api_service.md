---
title: "Python 後端 API 服務架構模式卡"
type: playbook
domain: "[[02-Areas/Software-Architecture/README]]"
tags: [architecture, playbook, python, fastapi, backend]
last_updated: "2026-11-24"
---

# ⚙️ 02. Python 後端 API 服務

## 1. 適用題型與禁用條件 (When to Use / When NOT to Use)
* **適用**：需對外提供穩定 HTTP / WebSocket 契約的 Python 服務（如 FastAPI 後端、VR/App 遠端服務、微服務）。
* **禁用**：一次性資料清理腳本、純離線 CLI 工具（直接單模組函式即可，勿硬套分層）。

## 2. 核心邊界與單向依賴 (Core Boundaries & Dependency Rule)
```text
entrypoints/ (FastAPI Routers + Pydantic DTOs + Depends 組裝)
    --> service_layer/ (Use Cases 用例編排 + Transaction / UoW)
        --> domain/ (純 Python 核心規則，零 FastAPI / ORM / HTTP 依賴)
adapters/ (DB Repositories + 外部 LLM / HTTP Clients) --實作抽象--> domain/service
```
* **依賴指向內層**：`domain/` 嚴禁匯入 FastAPI、SQLAlchemy 或外部 SDK，確保核心邏輯可無 I/O 秒級單測。
* **邊界契約分離**：API Request/Response 使用專用的 Pydantic DTO，不與資料庫 ORM Model 或 Domain Entity 混用。
* **顯式依賴注入**：透過 FastAPI `Depends`（或 Protocol 注入）在組合根組裝真實 Adapter，測試時替換為 Fake/In-Memory 實作。

## 3. 高頻反模式與爆點 (Failure Modes & Anti-Patterns)
* ❌ **Fat Router（路由寫死業務與 SQL）**：把規則、資料查詢、外部呼叫全寫在 `@router.post` 內，導致無法單測且改一處壞三處。
* ❌ **ORM Model 直出 API**：直接回傳資料庫物件，造成內部欄位洩漏、N+1 隱性查詢或 DB Schema 一改就炸毀對外契約。
* ❌ **全域單例地獄（Global Singleton）**：在模組載入時直接建立 DB 連線或 API Client，導致單元測試難以 Mock 與並發狀態汙染。
* ❌ **靜默吞錯（Bare Except）**：捕捉例外後只印 log 或回傳空值，掩蓋外部 API 超時與交易未回滾的真實故障。

## 4. Explore → Expand 演進門檻 (對齊 `GLOBAL-01`)
* **Explore 最小骨架**：維持 `routers` + `service` + `schemas` 三個清晰模組即可，先不強制引入抽象 Repository 與 UnitOfWork。
* **切換 Expand 紅燈**：出現多資料源切換、跨表交易原子性需求、或外部 I/O 阻礙自動化測試時，再抽出 Repository Protocol 與 UoW。

## 5. 開案必問 3–5 題 (Socratic Checklist for `grill-with-docs`)
1. **I/O 與超時邊界**：哪些外部呼叫（DB、LLM、第三方 API）會阻塞請求？需要 `async`、逾時上限或重試策略嗎？
2. **契約與版本穩定性**：誰是呼叫端（如 Unity VR / Mobile App）？錯誤碼與 JSON Response DTO 欄位有哪些不可破壞的約定？
3. **狀態與持久化**：資料只需記憶體暫存（Explore）、單機 SQLite，還是多實例共享 DB／Redis？
4. **驗證與安全邊界**：需要 Auth/Token 驗證、Rate Limiting 或對客戶端輸入做哪些防呆上限？

## 6. 權威出處 (Tier 1 / Tier 2 References)
* Harry Percival & Bob Gregory, *Architecture Patterns with Python (Cosmic Python)*
* FastAPI Official Docs, *Dependencies (`Depends` / `yield`)* & *Bigger Applications*
* Martin Fowler / Michael Nygard, *Architecture Decision Records (ADR)*
