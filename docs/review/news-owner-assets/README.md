# 最新消息：正式圖片替換

建立在使用者最新 `shinox-v2-hero` commit `a69b05f1b52c4f9109c4cd6f9d00e97f49ec71df` 上。保留已確認的卡片版型及中英文全部文章文案。

| 上傳 PNG | 正式 WebP | 使用位置 |
|---|---|---|
| ShinoX智慧洗車入口與車牌辨識 車尾版.png | lassets/news/shinox-anpr-entrance.webp | 中英文技術消息卡片縮圖、文章第一張主視覺 |
| 智慧洗車支付亭 去除設備版.png | lassets/news/shinox-cloud-payment-kiosk.webp | 中英文文章「選配觸控式雲端繳費機」區塊 |

原圖各自轉為 WebP quality 88，保留原始解析度，沒有重新生成、裁切或修改圖片文字；共 425,132 bytes。來源及輸出雜湊見 assets.json。第一份錯誤的 1029.zip 未使用。

僅更新圖片資產、圖片原生寬高與繳費機圖片的 contain／自然比例，避免繳費機及說明被既有 16:9 裁切。news-card-fix.css 與其載入版本、所有卡片文字、文章文字、連結、首頁、表單、後端及 Render 設定均保持基準版本不變。

## 驗證

- 中文／英文 × 1440px／390px，四組實際 Chromium 檢查。
- 技術縮圖及文章主圖確實載入車尾辨識 WebP；繳費機圖片完整顯示，沒有觸發舊 SVG／隱藏備援。
- 桌機三卡維持等高、16:9 及相同內距；手機保留使用者核准的最新單欄排版。
- 無圖片 404、JavaScript 錯誤或水平溢出；分類篩選、鍵盤開啟文章、文章中英切換通過。
- 全部 body 文字及連結與基準版本相同，見 scope-checks.json；量測及載入紀錄見 browser-qa.json。
- Sitemap 重建一致性檢查通過。未重新測試不受影響的後端功能，也未送出任何表單資料。

| 語系 | 三卡桌機 | 三卡手機 | 文章桌機 | 文章手機 |
|---|---|---|---|---|
| 繁中 | [截圖](zh-cards-1440.webp) | [截圖](zh-cards-390.webp) | [截圖](zh-article-1440.webp) | [截圖](zh-article-390.webp) |
| EN | [Screenshot](en-cards-1440.webp) | [Screenshot](en-cards-390.webp) | [Screenshot](en-article-1440.webp) | [Screenshot](en-article-390.webp) |

正式部署狀態請參閱 Issue #2 本批交付紀錄；GitHub 合併與私人驗收站發布不代表 Render 正式站已更新。
