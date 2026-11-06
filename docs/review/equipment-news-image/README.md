# 設備資訊：車輛長度自動感測技術

同步使用者最新 `shinox-v2-hero` 基準 `2def97fbb73ad38993f394fa7cd2f9631ad62d00`。

- 將 ZIP 內原始 `shinox-vehicle-length-detection.webp` 原封不動放入 `shinox-v2-site/lassets/news/`，2048 × 868px，157,348 bytes。SHA-256 與附件相同，沒有轉檔、重新生成或修改圖片。
- 設備資訊卡片沿用使用者最新版型及縮圖裁切；加入連到新文章的真正 HTML 連結和閱讀更多入口。
- 新增 `news-vehicle-length.html` 與 `en/news-vehicle-length.html`，完整整合使用者後續提供的正式內文及專業英文翻譯，共用既有技術文章視覺語言與同一份 CSS。
- 文章主視覺完整呈現原始寬幅圖；保留三階段原理、四項特色、品牌標語及實際規格限制說明。沒有新增未提供的技術參數或保證。
- 原技術消息卡片、車牌辨識圖、雲端繳費機圖及中英文智慧洗車文章逐位元組或 DOM 比對不變；首頁、表單、後端及 Render 設定不變，見 scope-checks.json。
- 新文章使用成對 canonical／hreflang；Sitemap 更新為 48 個正式中英文頁，重建一致性檢查通過。

## 實際驗收

瀏覽器紀錄見 browser-qa.json；素材來源見 asset.json；使用者原文與英文翻譯見 approved-copy.json。測試使用本機實際網頁，沒有送出真實表單資料。

| 頁面 | 中文桌機 | 中文手機 | 英文桌機 | 英文手機 |
|---|---|---|---|---|
| 新聞卡片 | [畫面](zh-cards-1440.webp) | [畫面](zh-cards-390.webp) | [Screen](en-cards-1440.webp) | [Screen](en-cards-390.webp) |
| 設備文章 | [畫面](zh-article-1440.webp) | [畫面](zh-article-390.webp) | [Screen](en-article-1440.webp) | [Screen](en-article-390.webp) |

私人驗收站發布與正式 Render 網站部署分別回報；不得將 GitHub 合併或私人站發布當作正式站已更新。實際發布狀態以 Issue #2 本批交付紀錄為準。
