# 最終驗收：政策頁、資源封面與兩處共用流程

所有截圖都是Chromium實際網頁，沿用網站原LOGO、共用樣式與同一份中英素材。政策與表單仍待營運驗收，線上收件關閉。

|項目|中文桌機1440px|中文手機390px|英文桌機1440px|英文手機390px|
|---|---|---|---|---|
|規劃旁3×2流程|[截圖](zh-planning-process-1440.webp)|[截圖](zh-planning-process-390.webp)|[Screenshot](en-planning-process-1440.webp)|[Screenshot](en-planning-process-390.webp)|
|原本橫向流程|[截圖](zh-original-process-1440.webp)|[截圖](zh-original-process-390.webp)|[Screenshot](en-original-process-1440.webp)|[Screenshot](en-original-process-390.webp)|
|隱私權政策|[截圖](zh-privacy-1440.webp)|[截圖](zh-privacy-390.webp)|[Screenshot](en-privacy-1440.webp)|[Screenshot](en-privacy-390.webp)|
|服務條款|[截圖](zh-terms-1440.webp)|[截圖](zh-terms-390.webp)|[Screenshot](en-terms-1440.webp)|[Screenshot](en-terms-390.webp)|
|首頁資源封面|[截圖](zh-resources-index-1440.webp)|[截圖](zh-resources-index-390.webp)|[Screenshot](en-resources-index-1440.webp)|[Screenshot](en-resources-index-390.webp)|
|聯絡頁資源封面|[截圖](zh-resources-contact-1440.webp)|[截圖](zh-resources-contact-390.webp)|[Screenshot](en-resources-contact-1440.webp)|[Screenshot](en-resources-contact-390.webp)|

## 驗收紀錄

- `qa.json`：56組頁面／尺寸檢查，涵蓋兩頁政策、clean URL與.html入口、中英、1440／768／390／375px、資源區及兩處流程；另有3組攔截式政策閘門／同意測試及1組正常動畫自動展示，共60筆。
- `process-final-qa.json`：補驗兩處流程、兩語言、四尺寸及手機／平板控制鈕避開浮動聯絡按鈕。
- `process-current-qa.json`：更新排版專用操作提示後的最後截圖與測試。
- 共用流程以原本可讀取的HTML內容為唯一內容來源，第二處以同一份JS元件建立，重新命名ARIA與節點ID，兩處狀態獨立。原處橫向、規劃旁3×2；手機先文案再流程。沒有背景圖片、水花、倒影或canvas。
- `legal-config.json` reviewAccepted=false；前後端都不因單獨開live旗標而收件。政策版本2026-10-29.1，確認欄未預選、非行銷同意，後端記錄政策版本、瀏覽器回報確認時間及獨立伺服器時間。
- 24項Python合成資料／mock SMTP測試通過；不代表正式寄信服務已啟用。
- 已檢查的51個主要HTML文件（含英文及內部管理頁）皆有兩個法律頁尾連結，4個目錄路由副本由同內容自動產生；25組中英版型與本機資源／錨點檢查通過。

## 其他本批內容

品牌介紹、事業方案、產品方案、專案案例／實例已整合使用者提供的原文與專業英文，見[內文截圖](../content-20261029/README.md)。網站圖片和設備參數未憑空更換。

兩張資源封面來自使用者上傳ZIP，優化後共約227KB；原圖未重新生成。ZIP沒有PDF，因此仍保留文件準備狀態，不提供假下載。

政策核對及待確認事項見[資料流稽核](../../PRIVACY_DATA_FLOW.md)。缺少公司／營運者、權利窗口及正式保留規則不妨礙頁面驗收，但在確認與核准前不開放真實收件。
