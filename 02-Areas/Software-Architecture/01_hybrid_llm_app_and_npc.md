---
title: "Hybrid LLM 互動應用 / Agent / 遊戲 NPC 架構模式卡"
type: playbook
domain: "[[02-Areas/Software-Architecture/README]]"
tags: [architecture, playbook, llm, npc, agent]
last_updated: "2026-11-24"
---

# 🤖 01. Hybrid LLM 互動應用 / Agent / 遊戲 NPC

## 1. 適用題型與禁用條件 (When to Use / When NOT to Use)
* **適用**：具狀態變化、經濟數值、遊戲規則或真實副作用（交易、議價、任務、工具執行）的對話與 Agent 系統（含 VR/即時互動 NPC）。
* **禁用**：單純一次性摘要／翻譯等無狀態純文字生成（無需 FSM 與多層架構）；或完全可由確定性規則／表單解決的靜態流程。

## 2. 核心邊界與單向依賴 (Core Boundaries & Dependency Rule)
```text
Client (VR/App)
  --> API Entrypoint
  --> 1. Intent Parser (Structured Output JSON Schema)
  --> 2. Deterministic Core (純 Python FSM / 數值與規則引擎，零 LLM)
  --> 3. Narrative Renderer (LLM 角色台詞 + 表情/動作標籤)
```
* **確定性核心層**：掌管金額、底線、耐心值、狀態轉移與權限；**成交與否、價格計算永遠由程式碼裁決**。
* **生成式渲染層**：僅負責把確定性結果轉譯為符合人格／職業口吻的台詞與表現訊號（`dialogue`, `mood`, `animation_trigger`）。
* **結構化契約**：輸入解析與輸出渲染皆強制走 JSON Schema（Structured Outputs / Pydantic 驗證），禁止靠正則從自由文字硬拆指令。

## 3. 高頻反模式與爆點 (Failure Modes & Anti-Patterns)
* ❌ **LLM 直改狀態／算數（Prompt Injection 破防）**：讓模型自行決定成交價或道具增減，玩家用話術即可「免費白拿」或誘發數值幻覺。
* ❌ **自由文字直連下游**：未做 Schema 約束與驗證就解析輸出，模型多一句寒暄即導致遊戲迴圈或前端崩潰。
* ❌ **盲目塞滿歷史脈絡（VR/即時互動延遲爆炸）**：把全劇本與長歷史塞進 Prompt 導致 TTFT 與回應超過 1–1.5 秒體感門檻，破壞沉浸感。
* ❌ **過早套用全自主 Multi-Agent 迴圈**：單純明確的 Workflow（Routing / Prompt Chaining）就能解決時硬上多 Agent，造成延遲倍增與除錯黑洞。

## 4. Explore → Expand 演進門檻 (對齊 `GLOBAL-01`)
* **Explore 最小骨架**：1 個無 I/O 的純 Python 狀態機模組 + 1 個可抽換的模型呼叫 Adapter（用假 LLM 測試狀態轉移）。
* **切換 Expand 紅燈**：需同時支援多連線 Session 持久化、切換本地 SLM（如 Ollama）壓低延遲、或引入串流語音 STT/TTS 管線時，再拆出 Session Store 與 Streaming Adapter。

## 5. 開案必問 3–5 題 (Socratic Checklist for `grill-with-docs`)
1. **規則與台詞邊界**：哪些狀態與數值（如底價、庫存、情緒門檻）必須 100% 由確定性程式控制、絕不交給 LLM？
2. **延遲與部署預算**：互動端允許的最大回應時間（RT / TTFT）是多少？選雲端 API 還是本地 SLM，上下文該如何修剪？
3. **多模態 I/O 邊界**：本服務只接收／回傳文字與結構化標籤，還是連語音辨識（STT）與合成（TTS）也要納入邊界？
4. **失敗降級策略**：當 LLM 逾時、斷線或回傳不合規 JSON 時，NPC 該如何給出安全的預設反應而不卡死流程？

## 6. 權威出處 (Tier 1 / Tier 2 References)
* Anthropic, *Building Effective Agents* (Workflows vs Agents, Start Simple)
* OpenAI, *Structured Outputs* & vLLM *Constrained Decoding* (JSON Schema Decoding)
* NVIDIA, *ACE (Avatar Cloud Engine)* (Deterministic Game Logic vs Narrative SLM Separation)
