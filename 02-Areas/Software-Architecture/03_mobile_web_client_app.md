---
title: "前端 / 手機 App 應用架構模式卡"
type: playbook
domain: "[[02-Areas/Software-Architecture/README]]"
tags: [architecture, playbook, frontend, react, react-native]
last_updated: "2026-11-24"
---

# 📱 03. 前端 / 手機 App 應用

## 1. 適用題型與禁用條件 (When to Use / When NOT to Use)
* **適用**：具非同步 API 存取、跨頁面共享狀態或行動裝置生命週期的互動應用（React、React Native / Expo）。
* **禁用**：純靜態展示頁或單頁簡單表單（直接使用單純元件與原生狀態即可，無須複雜快取庫）。

## 2. 核心邊界與單向依賴 (Core Boundaries & Dependency Rule)
```text
src/
├── features/<domain>/     # Feature-Based Colocation (UI + API Hooks + Utils + index.ts)
├── shared/                # 通用無業務邏輯 UI 元件、基礎 API Client、Theme
└── app/                   # 路由入口與全域 Provider (QueryClientProvider 等)
```
* **狀態二分法（Hard Split）**：
  * **Server State（遠端非同步）**：後端資料由快取層（如 TanStack Query）管理失效、重抓與去重，**嚴禁複製進全域 UI Store**。
  * **Client State（本地同步）**：Modal 開關、分頁 Tab、表單步驟等純介面狀態用 `useState` 或輕量 Store（如 Zustand）。
* **Feature 邊界隔離**：跨 Feature 僅能透過該資料夾根目錄 `index.ts` 匯入公開介面，嚴禁深層路徑互指。

## 3. 高頻反模式與爆點 (Failure Modes & Anti-Patterns)
* ❌ **把 API 資料塞進 Zustand / Redux**：手寫載入狀態、快取失效與競態處理，導致畫面顯示過期資料與大量樣板碼。
* ❌ **複製 Query 資料進 `useState`**：寫出 `const [item, setItem] = useState(data)` 製造雙重真源，背景更新後畫面不同步。
* ❌ **按檔案類型切資料夾（Type-Based）**：把所有 `components/`、`hooks/`、`services/` 堆在一起，改一個功能得跨五個目錄且無法安全刪碼。
* ❌ **忽略行動端生命週期**：在 React Native 中沿用網頁視窗焦點假設，未接上 `AppState`（前景／背景切換）與 `NetInfo` 斷網偵測。

## 4. Explore → Expand 演進門檻 (對齊 `GLOBAL-01`)
* **Explore 最小骨架**：按 Feature 建資料夾 + Typed `fetch` 封裝 + 局部 `useState`，先驗證核心互動流程。
* **切換 Expand 紅燈**：出現多頁面共享同一筆遠端資料、樂觀更新（Optimistic UI）、離線重試或效能掉幀時，再全面接入 TanStack Query 與嚴格 Barrel 檢查。

## 5. 開案必問 3–5 題 (Socratic Checklist for `grill-with-docs`)
1. **狀態歸屬盤點**：哪些資料是向後端借來的 Server State，哪些才是純前端 Client State？
2. **離線與弱網體驗**：Loading 骨架屏、錯誤重試、斷網降級或本地持久化（AsyncStorage / SQLite）的預期行為是什麼？
3. **平台與生命週期**：鎖定 Web、iOS/Android 原生還是跨平台（Expo）？背景切換或權限請求有哪些特殊處理？
4. **前後端契約對齊**：API Schema 未定案前，如何用 Mock Fixtures 讓前端獨立開發與測試？

## 6. 權威出處 (Tier 1 / Tier 2 References)
* TanStack Query Official Docs (*React Native Integration*, *Server vs Client State*)
* React / Expo Architecture Best Practices (*Feature-Based Colocation & Barrel Boundaries*)
