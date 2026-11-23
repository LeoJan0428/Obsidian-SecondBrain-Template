# 🧭 SecondBrain 決策作戰總覽儀表板 (Mission Control Dashboard)

> [!NOTE]
> 本儀表板由 **Dataview** 社群外掛驅動，自動動態彙整 `01-Projects/_active/` 與 `_inbox/` 狀態。
> 若畫面顯示原始碼區塊而非表格，請先確認已安裝並啟用 **Dataview** 外掛，並在設定中開啟 **Enable JavaScript Queries**。

---

## 📌 活躍專案作戰矩陣 (Active Projects Matrix)

```dataview
TABLE 
  status as "狀態",
  last_updated as "最後更新",
  repo_path as "程式碼倉儲",
  tech_stack as "核心技術棧"
FROM "01-Projects/_active"
WHERE file.name = "CONTEXT"
SORT last_updated DESC
```

---

## 📥 靈感與剪藏待消化隊列 (Inbox Queue)

```dataview
TABLE
  file.cday as "收集日期",
  tags as "標籤",
  source_url as "來源"
FROM "_inbox"
WHERE file.name != "README"
SORT file.cday DESC
```

---

## 🗺️ 空間白板總指揮所 (Spatial Canvas War Room)

- 🔗 **白板入口**：[[PROJECTS_WAR_ROOM.canvas|開啟專案作戰總白板 (PROJECTS_WAR_ROOM.canvas)]]

---

## ⚡ 專案即刻下一步行動 (Immediate Next Actions)

```dataviewjs
const pages = dv.pages('"01-Projects/_active"').where(p => p.file.name === "CONTEXT");

for (let p of pages) {
  try {
    const content = await dv.io.load(p.file.path);
    const match = content.match(/## 🚀 (?:即刻)?下一步行動[\s\S]*?(?=\n## |$)/);
    const projectName = p.project || p.file.folder.split('/').pop();
    
    dv.header(4, `🎯 [[${p.file.path}|${projectName}]]`);
    if (match) {
      const cleanAction = match[0].replace(/## 🚀 (?:即刻)?下一步行動.*?\n/, '').trim();
      dv.paragraph(cleanAction);
    } else {
      dv.paragraph("*(未設定即刻下一步行動)*");
    }
  } catch (err) {
    dv.paragraph(`*(讀取失敗: ${err.message})*`);
  }
}
```
