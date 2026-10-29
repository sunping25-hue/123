# 9 IN 1 首頁彈跳廣告：原圖已整合，實圖驗收通過

原先缺少原圖的阻礙已解除。本次使用業主新提供的官方 JPEG，與已核對的 9 IN 1 新產品上市英文形象照相同。沒有生成、重畫、裁切或替換成其他設備圖。

## 素材來源與完整性

- Google Drive 檔案 ID：`1bJGOTXChcD6kvXbvP3eH1_qu4qft9p3C`。
- 已驗證來源檔：`/workspace/123-favicon/shinox-v2-site/og-image.jpg`。
- 實際 Popup 路徑：`shinox-v2-site/lassets/campaign/9-in-1-new-product-launch.jpg`。
- 原生尺寸：**1200 × 630**。
- 來源與 Popup 檔案 SHA-256 相同：`96cce1e2686435ee12f9f56d800188233fbaaed0ad1d265e6a778e45fa94644b`。
- 直接複製原始 JPEG bytes，沒有重新編碼。設定已由未取得的 PNG 預留路徑改為實際 JPEG 路徑及正確寬高。

## 文案與功能

繁體中文主標維持「全新9合1智能洗車設備」。副標逐字保留：

> 歡迎來到ShinoX世界，這邊將滿足你自助洗車場建設需求，從洗車設備到場地規劃一次OK，我們擁有建設超過100場自助洗車場經驗，將協助你成功創業！

上述「超過100場」為業主指定文案，不是本次推定或新增的案例數字。英文維持既有對應翻譯。主標、副標及 CTA 都是獨立 DOM 文字；圖像保留官方英文形象照原稿。CTA「了解洗車設備」及英文按鈕實際連至同語系 `products/self-3.html`。

新活動 ID、原生模態、關閉、稍後、Escape、背景點擊、Tab 焦點循環、焦點復原與同分頁 session 頻率皆保留。廣告獨立於 Hero 及投資試算密碼視窗。

## 實際瀏覽器驗收

`copy-lifecycle-qa.json` 已更新為本次**真實原圖**驗收，原先 `BLOCKED` 狀態已解除。

- 中英文 × **1440×1000、390×844、375×667** 共六組通過。
- 圖片 HTTP 200、瀏覽器解碼原生 1200×630，下載 bytes 的 SHA 與原檔相同。
- `object-fit:contain` 顯示完整原圖；未使用假圖、攔截圖片請求或模擬圖片載入。
- 繁體中文逐字文案、英文翻譯、16px 內文及無橫向文字溢出通過。
- 關閉、稍後、Escape、背景點擊及同 session 不重複通過。
- Tab / Shift+Tab 雙向循環通過；CTA 實際導向正確中英文產品頁。
- 小螢幕內容可在模態內捲動，CTA 與稍後按鈕可到達。截圖包括初始圖文及捲動至操作位置兩種真實畫面。
- 無 JavaScript page errors。

| 語言／尺寸 | 初始畫面 | 操作位置 |
|---|---|---|
| 繁中 1440 | [截圖](zh-1440.webp) | [操作](zh-1440-actions.webp) |
| 繁中 390 | [截圖](zh-390.webp) | [操作](zh-390-actions.webp) |
| 繁中 375 | [截圖](zh-375.webp) | [操作](zh-375-actions.webp) |
| English 1440 | [Screenshot](en-1440.webp) | [Actions](en-1440-actions.webp) |
| English 390 | [Screenshot](en-390.webp) | [Actions](en-390-actions.webp) |
| English 375 | [Screenshot](en-375.webp) | [Actions](en-375-actions.webp) |

## 保護範圍與部署狀態

Hero、兩個首頁 HTML、表單頁、`site.js`、投資密碼流程 JS 與 `render.yaml`，均逐檔與權威基底 `84c2890364405673468d2f28f2d3f2b8f781daad` 比較 bytes 完全一致；詳見 `protected-files.json`。本次不改寫其他產品頁或既有實作。

**尚未部署。** 本批僅建立本機提交，沒有遠端推送、GitHub／PR 修改、私人站發布、Render 發布或合併。後續由主代理審閱及執行已授權的預覽發布；本文件不宣稱任何正式網站已更新。
