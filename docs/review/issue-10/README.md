# Issue #10：九合一洗車控制箱雙語互動產品頁

保留原有入口 `products/self-3.html` 與 `en/products/self-3.html`，沿用正式 LOGO、導覽、頁腳、LINE／WhatsApp、投資工具及詢價連結。實作為真正 HTML／CSS／JavaScript，沒有使用整張設計稿、image map 或圖片文字冒充介面。

## 十區塊完成清單

- [x] 01 Hero：核准的原始設備圖、左文右圖的響應式構圖／手機上下排列、四個 SVG 賣點與官方 LINE CTA。
- [x] 02 產品優勢：四個真實卡片、SVG、Hover／Focus 與配置限制。
- [x] 03 外觀款式：四個規劃色票、按鈕／鍵盤與 aria-pressed 同步；產品原圖不改色，供應與正式照片明確待確認。
- [x] 04 操作介面：九個獨立 HTML 功能按鍵及狀態說明；未確認第九項保留為預留示意，不捏造正式功能。
- [x] 05 濕區：功能清單、SVG 情境與待確認配置，沒有宣稱九項標配。
- [x] 06 乾區：獨立功能卡與選配標籤，未確認功能以擴充規劃呈現。
- [x] 07 多元支付：四種方式與 SVG；支付、會員及開通依配備／整合而定。
- [x] 08 功能設定：原生數字欄位、吃到飽／暫停切換、驗證、套用及重設；僅本頁記憶體，沒有 API／實體設備操作。
- [x] 09 外接擴充：兩個獨立示意模組及 SVG 連線，不代表固定兩個實際輸出端口。
- [x] 10 雲端管理：真正 DOM 指標及日／週動態圖表，明確標示模擬資料與選配，沒有真實營運績效宣稱。

註：吃到飽為「設定時長內使用」的介面示意，切換不會把時長變成不限時。金額欄使用示範點數，不是售價或收費設定。

## 驗證

- Chromium 中英文 × 1440／1024／768／390px，共 **8 組完整互動驗證通過**。
- 色票四選一、鍵盤方向／End、原產品圖不變；全部九個功能的選取與說明；時間／點數必填、上下限、步進與小數錯誤；Enter 套用、重設；吃到飽保留時長；日／週模擬數據及圖表 ARIA。
- 10 個 section 皆存在、圖片解碼、無水平／文字溢出、JS 錯誤或 HTTP 失敗；示意設定沒有 POST 請求。兩語主內容與動態狀態分別完整翻譯。
- `node --check products/nine-control.js`、`git diff --check`、48 正式頁索引一致性檢查通過。
- 15 個受保護檔案雜湊不變：首頁、產品列表、新聞、Google 試算表表單、後端與部署設定，見 protected-files.json。
- 既有自助設備列表仍連到相同產品路徑；原詢價／LINE／WhatsApp 及頁尾流程保留。手機互動區保留浮動聯絡按鈕安全間距。

完整量測及互動紀錄：[browser-qa.json](browser-qa.json)。實體 iOS／Android 尚需人工驗收，不將 Chromium 視窗模擬當作真實裝置。

| 內容 | 中文桌機 | 中文手機 | English desktop | English mobile |
|---|---|---|---|---|
| 整頁十區塊 | [畫面](zh-page-1440.webp) | [畫面](zh-page-390.webp) | [Screen](en-page-1440.webp) | [Screen](en-page-390.webp) |
| Hero | [畫面](zh-hero-1440.webp) | [畫面](zh-hero-390.webp) | [Screen](en-hero-1440.webp) | [Screen](en-hero-390.webp) |
| 操作介面 | [畫面](zh-interface-1440.webp) | [畫面](zh-interface-390.webp) | [Screen](en-interface-1440.webp) | [Screen](en-interface-390.webp) |
| 設定 | [畫面](zh-settings-1440.webp) | [畫面](zh-settings-390.webp) | [Screen](en-settings-1440.webp) | [Screen](en-settings-390.webp) |
| 雲端示意 | [畫面](zh-cloud-1440.webp) | [畫面](zh-cloud-390.webp) | [Screen](en-cloud-1440.webp) | [Screen](en-cloud-390.webp) |

## 尚缺原始素材及規格

Issue #10 內文與留言沒有實際 1～10 設計圖，專案中亦未找到對應原檔，因此未宣稱已逐張比對或達到像素還原。當前依任務書製作十區塊，使用已核准控制箱原圖；濕／乾區沒有正式現場照片時使用真正 SVG／DOM 情境示意。

精確補件建議見 [asset-audit.md](asset-audit.md)：

| 缺件 | 建議尺寸 | 目標路徑 |
|---|---|---|
| 原 1～10 設計圖 `nine-in-one-reference-01-10.png` | 原尺寸，長邊至少 2400px | `docs/references/`，僅內部比對 |
| 銀／藍／黑／紅核准實照 `nine-in-one-{silver,blue,black,red}.webp` | 各 1200×1200 | `shinox-v2-site/lassets/products/nine-in-one/` |
| 濕區及乾區授權場景 `nine-in-one-{wet-zone,dry-zone}.webp` | 各 1600×1000 | 同上 |
| 已確認規格／功能與選配表 `nine-in-one-confirmed-specs.pdf` | PDF | `docs/source/` |

缺件不阻塞已完成的網頁元件與互動；實際設備功能、顏色供應、輸出端口、支付及遠端支援仍須正式資料確認。

## 發布範圍

此批提交獨立功能分支及 PR，更新既有 owner-private Sites 驗收站；不合併其他草稿，不修改 main，不把私人預覽發布稱為 Render 正式站上線。實際預覽 URL／版本／部署紀錄見 Issue #10 交付留言。
