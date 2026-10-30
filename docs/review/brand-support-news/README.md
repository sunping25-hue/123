# 品牌動態：原廠技術交流與開店輔導

本批依使用者核定的完整品牌文章與最新正式 RAR 四圖實作，基底為 `32c8f18`。僅更新中英文消息列表的品牌卡片、新增雙語文章、品牌文章限定 CSS、兩筆 sitemap URL 與審閱素材；沒有修改設備資訊／技術消息卡片及其文章和圖片，亦沒有修改首頁 Hero 或聯絡表單。

## 路徑

- 繁中：`news-beyond-the-machine.html`
- English：`en/news-beyond-the-machine.html`
- 列表入口：`news.html`／`en/news.html` 的「品牌動態」卡片與既有分類篩選。
- Canonical／中英 hreflang／x-default 使用正式網址 `https://www.shinox-wash.com/`；這是原始碼設定，不代表本批已發布。
- Sitemap 僅增加兩個對應 URL，lastmod 為 2026-10-30；文章未添加未經提供的發布日期。

## 文案與結構

- 繁中標題逐字保留：「買洗車機，不只是買設備！ShinoX 原廠技術交流與開店輔導一次到位」。
- 英文標題：「More Than a Car Wash Machine — ShinoX Technical Support & Business Guidance」。
- 完整正文包含開場、原廠技術交流群組五項內容、開店輔導手冊八主題 SVG 卡片、長期服務四圖示、原文服務組合標語及聯絡 CTA。
- 保留所有資格及合約說明：符合方案始具加入資格；群組交流不另收參與費，但維修／零件／到場服務及保固依合約；法規為一般資訊，申請與合法性仍須專業確認；非不限次數免費維修承諾，亦不保證獲利或核准。
- 正文是可選取的真實 HTML，英文全文、卡片、按鈕與 alt 為人工對應翻譯。三張文章圖片與一張僅供列表使用的縮圖皆為業主提供形象圖，沒有生成或虛構新增案例。
- `source-copy-qa.json`：由使用者完整繁中 Markdown 核對 55 個文字段落／欄位，全數存在。八個手冊主題的標題和說明分開核對，沒有省略詞句。
- `approved-copy.json` 保存雙語實作文字供審閱，不代表本次獨立查驗公司的服務紀錄或承諾。

## 最新正式素材

檔案來源／原始與 WebP SHA 見 `asset-audit.json`。最後一批 RAR 與先前相同四個圖像 payload，但有三個檔名重新對應，已依最新指定映射更新並重拍全部截圖。

| 路徑（`lassets/news/brand-support/`） | 尺寸 | 對應 |
|---|---|---|
| `thumb-support.webp` | 1200×675 | 僅品牌卡片縮圖，不放入文章 |
| `technical-community.webp` | 1672×941 | 原廠技術交流群組 |
| `business-guide.webp` | 1672×941 | 開店輔導手冊 |
| `service-ecosystem.webp` | 1672×941 | 長期營運支援 |

列表卡片沿用原有 16:9 thumbnail／相同 padding 與伸展高度。文章只依指定順序放入三張不重複圖：`technical-community.webp` → `business-guide.webp` → `service-ecosystem.webp`；不額外插入 `thumb-support.webp`。三張文章圖片採自然比例與 `object-fit:contain`，完整顯示內容並使用 lazy loading。

## 實際瀏覽器驗收

最終素材驗收：中英文 × 1440／390，共四組通過。移除額外文章縮圖並將英文身分敘述統一為 ShinoX technical team/support community 後，只重拍與重驗四組受影響文章；不重複執行未變動的列表篩選。原列表驗收及未修改證明仍保留，詳見 `browser-qa.json`。

- 三張指定文章圖 HTTP 200、成功 decode、正確原生尺寸及描述 alt，完整 contain；列表縮圖亦已通過原先的 HTTP／decode 驗收。
- 標題與完整核定文案、8 個手冊卡片、5 個交流項目、4 個服務圖示通過。
- 桌機三卡等高、同 16:9 圖框；手機及桌機無頁面／文字水平溢位。
- 品牌／設備／技術三分類篩選正常，品牌卡片 Enter 鍵可進文章。
- 文章中英文切換維持同篇文章，聯絡 CTA 實際導向同語系聯絡頁；沒有提交外部表單。
- 無 JavaScript page errors。
- `preservation` 逐位元組比較證明設備／技術兩卡、兩組既有文章、原圖、首頁、聯絡頁及 Hero MP4 與 `32c8f18` 相同。

| 畫面 | 桌機 | 手機 |
|---|---|---|
| 繁中列表三卡 | [1440](zh-cards-1440.webp) | [390](zh-cards-390.webp) |
| 繁中完整文章 | [1440](zh-article-1440.webp) | [390](zh-article-390.webp) |
| English cards | [1440](en-cards-1440.webp) | [390](en-cards-390.webp) |
| English full article | [1440](en-article-1440.webp) | [390](en-article-390.webp) |

本代理未暫存、提交、推送或發布。交由主代理審閱及處理後續 PR／私人預覽；沒有宣稱 Render 正式網站已更新。
