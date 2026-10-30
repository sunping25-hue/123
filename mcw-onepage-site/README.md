# MCW 魔彩自助洗衣：加盟一頁式網站

純 HTML / CSS / 少量 JS，沒有建置步驟，也不用任何付費服務。

- `index.html`：14 個區塊，內容依 copy_v1.md；FAQ JSON-LD 用於 SEO
- `style.css`：亮色主題，主色 #1E3FA8 藍、#E5322D 紅、#F4F6FA 底色；斷點 ≥1024、768–1023、≤767
- `calc.js`：試算公式（UMD，測試時用 node 執行）；`app.js`：試算器 UI、門市輪播、預約表單
- `config.js`：表單送出位置（`formEndpoint`）
- `img/`：每張圖都有 WebP 和 JPG 備援，只縮小尺寸，沒有調色

本機預覽：`python3 -m http.server`，然後開 http://localhost:8000/
測試：`python3 tests/test_mcw_onepage.py`

## 表單送出（免費做法：Google 試算表 + Apps Script）
1. 建一個 Google 試算表，到「擴充功能 → Apps Script」，貼上下面的程式：
```js
function doPost(e){const d=JSON.parse(e.postData.contents);const s=SpreadsheetApp.getActiveSheet();
s.appendRow([new Date(),d.name,d.phone,d.line,d.city,d.hasStore,d.time,d.interest,d.page]);
return ContentService.createTextOutput('ok');}
```
2. 部署為「網頁應用程式」：執行身分選「我」，存取權選「所有人」。複製產生的 `/exec` 網址。
3. 把網址填入 `config.js`：`window.MCW_CONFIG={formEndpoint:'https://script.google.com/macros/s/…/exec'}`。
還沒設定網址時，表單會提示訪客直接加 LINE @mcw27 或撥打加盟專線。

## 待老闆確認的佔位內容
目前這些都隱藏或留白，不會顯示在頁面上；搜尋 `hidden` 或 `data-placeholder` 就能找到。
- Logo 與吉祥物圖檔（目前用文字 logo）
- 紫外線燈功能是否標配
- 寵物地墊專用機
- 雙層烘衣機照片
- 行動支付（FAQ 第 6 題）
- 第 7 區「周邊設備」
- 7×24 客服
- ISO 證書圖片；CE、45001、14001、專利、美國外銷資料
- 五甲店的機台配置與開幕年月
- 另外 4 間門市資料，以及哪些門市可以預約參觀
- 保固條款細節
- 試算器的數值範圍與預設值（目前金額欄位都空白）
- 表單送出網址
- 隱私權政策頁面
- 「上海工廠製造，科嘉國際台灣總代理」的寫法
- 洗脫烘一體機照片上的「新產品準備發表」字樣是否可用
