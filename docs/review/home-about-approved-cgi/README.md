# 首頁02 / ABOUT SHINOX｜使用者正式CGI整合

|語言|桌機1440px|手機390px|
|---|---|---|
|繁體中文|[實際截圖](zh-1440.webp)|[實際截圖](zh-390.webp)|
|English|[Screenshot](en-1440.webp)|[Screenshot](en-390.webp)|

## 完成內容

- 使用上傳 `about-hero.webp.zip` 內四張PNG原圖，不重新生圖、不使用外部照片。
- about-hero → 大型品牌主視覺；about-equipment → EQUIPMENT；about-integration → INTEGRATION；about-global → CONVERSATION。
- 圖片存入 `shinox-v2-site/lassets/home/about/`，清楚命名 `home-about-{hero,equipment,integration,conversation}.webp`，另有small版本。八個WebP合計762,836 bytes；瀏覽器依srcset選擇其中一個尺寸，不會一次載入全部版本。
- 桌機非對稱45/55雙欄，底部三張等寬圖卡；手機依序為標題、原介紹文字、主視覺、兩個CTA、單欄三卡。object-fit:contain保留完整原圖，文字均為HTML。
- 進場淡入、三卡90ms間隔、最大6px視差、Hover圖片微放大與邊框增亮。減少動畫時不隱藏文字、不做視差或縮放。
- 事業方案及YouTube連結維持原值；YouTube另開新頁並設noopener noreferrer。

## 修改檔案

- `shinox-v2-site/index.html`、`en/index.html`：只更新首頁02區塊及其必要CSS/JS引用。
- `shinox-v2-site/home-about.css`：限定此區的雙欄、圖卡、手機順序與動態。
- `shinox-v2-site/home-about.js`：IntersectionObserver淡入、事件驅動的微視差、偏好處理。
- `shinox-v2-site/lassets/home/about/*`：四張使用者圖的兩種WebP尺寸。
- `shinox-v2-site/locales/en.json`、`en.js`：四張圖片的英文替代文字。
- `scripts/build_english.py`：響應式srcset候選路徑與英文版共用資產。
- `scripts/check_bilingual_assets.py`：驗證srcset檔案存在，防止英文相對路徑造成破圖。
- `docs/HOME_ABOUT_APPROVED_CGI_UPLOAD.json`：原始來源與各輸出尺寸、大小及SHA。

## 實測

`qa.json`：1920、1440、1024、768、390、375px，中英文共12組RWD檢查，加正常動畫／點擊測試。四圖載入、桌機欄比、手機閱讀順序、三卡排列、文字邊界、減少動畫與表單停用皆通過；沒有水平溢出或JS錯誤。正常模式驗證淡入、0/90/180ms卡片進場、微視差變化、1.035倍Hover及偏好切換。實際點擊進入business.html；YouTube新分頁指向官方頻道且opener=null（目的頁測試以攔截方式驗證，不向外部網站傳送表單資料）。

額外比對：首頁其他九個main區塊DOM逐一與修改前一致；legal-config.json及api/status與修改前位元組完全相同。未更改表單開放狀態。

## 本批稍早已授權的事業頁修改

- 刪除「正在規劃5–20格」旁的新增流程，文案及兩個按鈕保留；下方原有六階段流程保留，檢查八組尺寸／語言。
- 以使用者上傳的夜間工作室洗車場模型替換5–20格規劃旁圖，1536×1024、WebP355,368 bytes，中英共用。文案、按鈕與概念圖說保留。
- [規劃新圖桌機](../site-planning-maquette/zh-1440.webp)／[手機](../site-planning-maquette/zh-390.webp)。來源及SHA見 `docs/SITE_PLANNING_MAQUETTE_UPLOAD.json`。
