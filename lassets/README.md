# lassets — ShinoX V2.0 非 Hero 圖像素材庫

此目錄集中存放**落地頁首屏 Hero 以外**需要展示的原創 AI 插畫、CGI 概念圖、縮圖、產品頁視覺及其他媒體。官方 LOGO 和 Hero MP4 原有檔案路徑不變；本次不修改 Hero。

## 風格
高階工業科技 CGI；深海軍藍、電光藍、冰藍、青綠、鈦銀；玻璃/金屬/液體質感；精確光影、低噪、品牌一致。不製造假證照、誇大規格、假客戶或假完工實績。AI 概念圖不得誤稱為真實產品照片。

## 素材命名與目錄
- `lassets/brand/` — 品牌理念、工程研發抽象插畫
- `lassets/solutions/` — 三大產品分類示意插畫
- `lassets/elements/` — 五元素科技動畫/靜態備援
- `lassets/business/` — 自助洗車場場地規劃/整合 CGI
- `lassets/products/` — 產品專題 CGI：**只可用經使用者確認的真實設備參考圖進行精準建模**
- `lassets/news/` — 消息內容對應插畫，須有真實發布內容
- `lassets/cases/` — 只放經核實的真實案例/授權照片；未核實案例不得生成偽實績

### 首輪落地頁圖像清單
| ID | 圖片位置 | 建議檔名 | 圖像內容 | 實作狀態 |
|---|---|---|---|---|
| A1 | 品牌理念 | `brand/innovation-cgi.webp` | 金屬流線、微型粒子與藍綠能源脈動 | 待生成/上傳 |
| A2 | 自助洗車設備分類 | `solutions/self-service-cgi.webp` | 自助洗車站抽象概念視覺，不冒充實際商品 | 待生成/上傳 |
| A3 | 自動洗車設備分類 | `solutions/automatic-cgi.webp` | 智慧無接觸洗車科技概念視覺，非實際機型 | 待生成/上傳 |
| A4 | 周邊設備分類 | `solutions/accessories-cgi.webp` | 工業零部件/感測元件抽象技術插畫 | 待生成/上傳 |
| A5 | 事業方案 | `business/site-planning-cgi.webp` | 洗車場規劃 CGI，須註明示意圖 | 待生成/上傳 |
| A6–A10 | 五元素 | `elements/{metal,energy,air,water,fluid}.webp` | 五種不同科技元素 CGI | 待生成/上傳 |

## 執行規則
1. 先盤點 `index.html` 全部非 Hero 圖像位置。現版本除了 Hero poster 和官方 LOGO，**尚未有實際圖片庫素材**；因此任務包含「建立圖片展示區＋生成素材＋替換引用」，不是假設已有相片可替換。
2. 使用圖像生成模型**原創生成**每張非 Hero 圖，不使用隨機外部庫存圖。
3. 生成後審核是否與文案、配置、設備真實性相符；失真就重製，不能隨便用 AI 編造產品外觀。
4. 每個檔案優先提供 WebP（或 AVIF）以及清楚的 `alt` 文案、寬高，非首屏 lazy load。
5. 檔案上傳 GitHub 後才將頁面路徑更新為 `lassets/... `。禁止留下不能載入的圖片路徑，或用沒有真正上傳的圖片宣稱已完成。
6. 必須瀏覽器檢查桌機 1440px、平板 768px、手機 390px，並提供圖片載入與效能驗收結果。
7. **Hero 首屏例外**：不替換 `media/shinox-hero.mp4`、`media/shinox-poster.jpg` 或品牌 LOGO；它們由使用者提供，另行整合。

設計/功能依據：`docs/SHINOX_V2_MASTER_PLAN.md`。


## Required color/material balance — approved visual reference
The user explicitly noted that earlier page mockups underused **teal-green and titanium/silver metallic surfaces** relative to the approved Hero reference. Correct this across all below-Hero illustrations and UI, not by changing the approved Hero itself.
- Visual-emphasis target **45% electric blue (#087CFF), 25% teal/turquoise (#17DDC7), 30% titanium silver/chrome (#C8D7E6 with metallic gradients)** among lit CGI subjects. This is a design guideline **for focal visual subjects**, NOT a whole-page pixel quota. Dark navy/near-black remains the dominant background.
- Make titanium silver tangible and prominent on turbines, machined edges, product enclosures and mechanical structures; use physically plausible glossy gradients and highlights.
- Make luminous teal streams clearly visible next to electric-blue water and energy ribbons. Avoid monochromatic cobalt-blue pages.
- Implement a reusable token set for navy, electric blue, teal, silver, and surface/highlight gradients; check all non-Hero visuals for this palette.
- The last user-provided Hero reference image is the **color/material benchmark**. Preserve its right-side crystalline turbine, visible teal streams, chrome surfaces, luminous flowing water.
