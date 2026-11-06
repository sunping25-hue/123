# ShinoX — 已購買網域，Render 正式網站部署準備（2026-10-29）

## 狀態
業主表示已購買 **shinox-wash.com**。尚未驗證 DNS、Render 主機、HTTPS、正式網址或個資表單。**不要宣稱正式上線完成**。本次部署只允許公開展示網站，`SHINOX_DEPLOY_STAGE=preview`、`SHINOX_FORM_LIVE=0`，不接受真實個資；保留現有 main、舊站、私人預覽站與 GitHub issue #2。

## 1. Cloudflare 網域
- 由業主在自己的 Cloudflare 帳號確認 `shinox-wash.com` 已在網域列表，啟用 2FA、auto-renew、正確的註冊聯絡 Email。
- 目標主要網域 `https://www.shinox-wash.com`，裸網域 `https://shinox-wash.com` 轉址至 www。先完成 Render 網域驗證及 HTTPS，再做轉址。
- DNS 記錄必須採 Render Custom Domains 畫面實際提供的值，不要猜測 IP、CNAME 或代理狀態；檢查與其他紀錄衝突。

## 2. Render Blueprint（先公開展示、不收件）
- 由業主登入 Render，連接 GitHub `sunping25-hue/123`，選擇 Blueprint 並指向 `shinox-v2-hero` 分支的 `render.yaml`。
- Singapore 區域、Starter 付費 Web Service、1GB 私有磁碟、手動部署。**建立服務及磁碟會產生費用，需由業主自行確認付款**。
- 起動腳本 `scripts/start_render.py` 監聽 `0.0.0.0:$PORT`；`SHINOX_DB_PATH=/var/data/requests.sqlite3`。
- `SHINOX_DEPLOY_STAGE=preview`：使用不接受表單的展示模式，不需要 SMTP 或管理金鑰；`/api/status` 應為 `acceptingLeads:false`。
- 此階段不應設定 `SHINOX_DEPLOY_STAGE=production`、`SHINOX_FORM_LIVE=1` 或開放管理頁。
- Render 自動提供 `onrender.com` 測試網址，先測試站點內容，再於 Settings > Custom Domains 新增 `www.shinox-wash.com` 及 `shinox-wash.com`。依 Render 顯示值設定 Cloudflare DNS，等待憑證生效。
- 不得將 Render、Cloudflare、SMTP 帳號密碼、金鑰貼在聊天或提交 GitHub。

## 3. 公開展示站驗收
- 首頁與七大頁面、中文/英文、手機版、產品圖片、Hero 影片、聯絡 CTA、404、法律頁、SEO 與 HTTPS 實測。
- `GET /api/status` 顯示 `acceptingLeads:false`；任何 `POST /api/leads` 或 `/api/booking-requests` 必須拒絕。頁面應明確引導使用者以 LINE、電話或 WhatsApp 聯絡。
- 不能因 GitHub 程式碼提交或 CI 通過就宣稱網站已經正式公開；須實際測試 Render URL 與正式網域。

## 4. 未來才啟用表單
待 `docs/PRODUCTION_LEADS.md` 和 `docs/PRIVACY_DATA_FLOW.md` 全部完成：業主個資政策核准、持久化資料庫、加密異地備份、管理權限、HTTPS、真實 SMTP 雙收件人測試、虛構資料端到端驗收，才能將 `SHINOX_DEPLOY_STAGE=production`，在 Render 的秘密環境變數設定 `SHINOX_PUBLIC_ORIGIN=https://www.shinox-wash.com`、SMTP 和至少 32 字元的管理金鑰。此時仍應先保持 `SHINOX_FORM_LIVE=0`，直到最終核准後才設為 1。

## 5. 注意
- 現在的 Python HTTP Server 為內建服務，正式大量流量與安全性仍須評估；Render HTTPS 不等於應用層安全審查完成。
- SQLite 磁碟不支援跨實例共享；主機重啟及資料備份必須實測。
- 主機、磁碟與網域可能另行計費，不能在未經業主授權下建立資源。

官方文件：https://render.com/docs/blueprint-spec 、https://render.com/docs/web-services 、https://render.com/docs/custom-domains 、https://developers.cloudflare.com/registrar/
