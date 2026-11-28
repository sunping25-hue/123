# Google 試算表洽詢表單

使用業主指定 Apps Script Web App；僅修改 `site.js` 與 `index.html`、`contact.html`、`en/index.html`、`en/contact.html` 內的 `#inquiry-form`。

## 內容

- 載入即啟用 Google Sheets 路徑，不再呼叫 `/api/status`；既有本機 API、Render 設定與政策檔完全不動。
- 新增必填「是否已有場地？」三選一，緊接所在地區。中英文提供指定文案，沒有預先選取。
- 保留未預勾的同意欄、政策版本、確認時間與 `website` honeypot；缺少同意／場地或命中 honeypot 不送出。
- POST 使用 `mode:no-cors`、`Content-Type:text/plain;charset=utf-8`、JSON body。`subject` 值放在 `model`；`description` 以現有需求說明 `message` 為預設。姓名／電話／Email／地區／場地／預約偏好、同意資料、表單類型／語言／頁面皆提供。
- 一般 lead 的預約欄位傳空字串；booking 傳入展示地點、日期、時段。成功重設欄位、單選、同意與表單模式；失敗保留輸入並顯示指定 LINE／電話提示。
- 送出中停用按鈕並避免重複送出。既有共用 UI 會將文字箭頭轉成相同視覺的 SVG，沒有修改按鈕樣式。

## 驗證結果

- 四個頁面 × 1440px／390px，**8 組瀏覽器情境通過**：啟用、必填、18 個 payload 欄位、所有場地選項、lead／booking、opaque response、成功重設、連線失敗、honeypot、連點防護。
- 所有 Google 請求均由 Playwright 攔截，僅使用合成資料，**沒有送出真實個資或測試列到試算表**。實際瀏覽器 response 為 `opaque` / status 0，測試驗證程式不讀取回應內容或 `response.ok`。
- 既有後端 24 項測試通過：server 12、production 9、policy 3。這驗證既有 API／收件保護未變動，不代表 Google 寫入成功。
- `node --check shinox-v2-site/site.js` 通過。
- 四頁表單以外的原始 HTML 位元組完全相同；原有 CSS、其他頁面、後端、Render、政策開關保持不變。
- 上游已新增新聞頁，但尚未同步 Sitemap／索引建置檢查；該既有問題未混入此五檔表單修改，另在 PR #6 有相容性修正。

[完整測試與請求資料](browser-qa.json)。可先在專案根目錄執行 `python server.py --port 3050`，再執行同目錄 `browser-qa.py`（需 Playwright 與 Chromium）。

| 頁面 | 桌機 | 手機 |
|---|---|---|
| 中文首頁 | [1440px](index-1440.webp) | [390px](index-390.webp) |
| 中文聯絡 | [1440px](contact-1440.webp) | [390px](contact-390.webp) |
| 英文首頁 | [1440px](en-index-1440.webp) | [390px](en-index-390.webp) |
| 英文聯絡 | [1440px](en-contact-1440.webp) | [390px](en-contact-390.webp) |

## 驗收限制

依業主指定，fetch resolved 時顯示「已收到…」。但 no-cors 不可讀取 Apps Script 的 HTTP 狀態／回應，**無法據此確認試算表實際新增資料列**；實際入表需由試算表擁有者確認。沒有宣稱已完成端到端入表驗收。

原隱私頁與政策設定依本次範圍保持不變；Google Apps Script／試算表的資料處理、保存及權利窗口仍需另行同步到政策。本次不修改它們，也不啟用既有 SQLite／SMTP 收件。

只合併 GitHub 開發分支，不觸發 Render 部署。
