# ShinoX — Render 正式上線準備（表單預設關閉）

## 狀態
這是部署準備，不是實際上線。**不得在尚未完成實際 HTTPS、SMTP、資料庫、個資告知與端到端驗收前收集真實個資**。本設定 `SHINOX_FORM_LIVE=0`；現有靜態驗收站不變。不要修改 main 或關閉 GitHub issue #2。

## 1. 網域
希望使用 `shinoxwash.com`，**尚未確認是否可註冊，也尚未購買**。由網站所有者登入 Cloudflare Registrar 搜尋並確認可用性、年費及續約價格，使用所有者本人帳號購買，啟用 2FA、自動續約及註冊信箱驗證。不要提供帳號密碼或付款資料給開發者。先不要設定正式 DNS。

## 2. Render Blueprint
- 在 Render Dashboard 以自己的帳號連接 GitHub repo `sunping25-hue/123`。
- 選擇 Blueprint，使用分支 `shinox-v2-hero` 根目錄的 `render.yaml`。
- 此設定建立 Singapore 地區 Python Web Service、Starter 付費方案、1GB 私有持久化磁碟（`/var/data`）、手動部署，並把表單設為關閉。建立 Blueprint 可能產生費用，需由所有者確認。
- 啟動程式 `scripts/start_render.py` 使用 Render 的 `PORT`，對 `0.0.0.0` 監聽，資料庫路徑為 `/var/data/requests.sqlite3`。
- `SHINOX_PUBLIC_ORIGIN` 要填經確認的正式 HTTPS 網域，例如 `https://www.shinoxwash.com`；必須與實際前端網址完全相符。
- Render 的 `onrender.com` 預設網址可用於**不收件**的外觀與 API 狀態測試；正式站應設定主網域與 www 統一轉址，避免 origin 不一致。
- 在 Render Dashboard 的 Environment 中填入 SMTP host/user/password/from 及長度至少 32 的 `SHINOX_ADMIN_TOKEN`。沒有有效設定時程式會拒絕啟動，這是預期的 fail-closed 行為。**不得把憑證提交 GitHub 或貼在聊天**。
- 連接 Render Custom Domains，再依 Render 提供的實際 DNS 記錄於 Cloudflare 設定。不要猜測 IP、A/CNAME 值。等待 Render 驗證與 HTTPS 生效。

## 3. 開站驗收（表單仍關閉）
- Render service 正常運行；`/api/status` 需回應，`acceptingLeads:false`。
- 中文/英文導覽、手機版、圖片與影片、產品 CTA、404、法律頁、站點 SEO 及自訂網域 HTTPS 實測。
- 任意表單提交必須被拒絕，不能收集真實資料。
- 正式啟用前必須另依 `docs/PRODUCTION_LEADS.md` 與 `docs/PRIVACY_DATA_FLOW.md` 完成合法告知、保留政策、備份、權限、SMTP 真實雙收件人送達及虛構資料 E2E 測試；最後才由業主核准 `SHINOX_FORM_LIVE=1`。

## 4. 安全與營運注意
- SQLite 僅適合目前單實例部署；Render 磁碟不支援多實例共享，附磁碟部署可能短暫停機。
- Render 自動磁碟快照不應被當成完整、可獨立還原的離站備份；仍須建立加密異地備份、保留與刪除流程。
- 目前服務採 Python 內建 HTTP server，正式對外使用前需另評估安全、效能、反向代理及濫用防護；Render 終止 HTTPS 不等於完成所有應用層安全驗收。
- Render Blueprint 建立或調整可能計費。不要在未經所有者同意下建立付費資源。

官方文件：
- https://render.com/docs/blueprint-spec
- https://render.com/docs/web-services
- https://render.com/docs/disks
- https://developers.cloudflare.com/registrar/get-started/register-domain/
