# ShinoX 正式表單：部署與驗收閘門（2026-10-29）

## 現況與上線限制

此分支提供正式表單後端程式，但**尚未部署至正式 HTTPS 伺服器**。私人靜態驗收站的 `/api/status` 仍為 `static-review`、`persistence:false`，不接收任何真實個資。不得將「程式已提交」當作「已上線」。

既有 `server.py` 本機模式保留測試用途。正式模式必須明確加 `--production` 並滿足所有環境設定；`SHINOX_FORM_LIVE` 預設為 0。前端僅在 `mode=production`、`persistence=true`、`emailConfigured=true`、`acceptingLeads=true` 同時成立時開放送出。

## 收件、儲存、通知

- `POST /api/leads`：設備與建場諮詢。
- `POST /api/booking-requests`：展示洽詢，不保證場地、日期或時段。
- SQLite 必須存放在主機的**持久化私有磁碟**，不得位於 Git 專案或網站靜態根目錄；申請和通知待辦在單一交易寫入。
- 兩個固定通知信箱：`shinox.car.washer@gmail.com`、`sunping25@gmail.com`。SMTP 連線失敗時仍保留已儲存的案件，背景每 60 秒重試，指數退避，最多 12 次。管理頁可查看未寄送狀態；超過重試上限必須人工處理。
- 資料保留 30 天，正式模式每 60 秒清除逾期資料；**已寄出的 Email 副本與備份必須另外管理其保留及刪除**。上線前應取得業主對保留政策、個資告知和管理權限的確認。
- `GET /api/admin/leads`：Bearer 金鑰驗證後取得最新 200 筆；`GET /api/admin/export.csv`：同樣驗證並匯出最新 200 筆。管理介面：`/admin.html`。CSV 防公式注入。請不要將管理金鑰放在網址、前端程式、Git 或分享訊息。
- 每 IP 10 分鐘最多 10 次、同來源檢查、蜜罐、內容大小限制、伺服器驗證；正式站仍應加上反向代理/WAF、監控與 HTTPS。
- 備份：`SHINOX_DB_PATH=... SHINOX_BACKUP_DIR=... python scripts/backup_leads.py`，備份檔案也包含個資；需配置定時執行、加密儲存、備份輪替與還原演練。

## 伺服器環境設定（不要提交實際密碼）

```sh
SHINOX_PUBLIC_ORIGIN=https://your-verified-domain.example
SHINOX_DB_PATH=/var/lib/shinox/requests.sqlite3
SHINOX_SMTP_HOST=smtp.your-provider.example
SHINOX_SMTP_PORT=465
SHINOX_SMTP_USER=your-smtp-user
SHINOX_SMTP_PASSWORD=secret-from-host-vault
SHINOX_SMTP_FROM=verified-sender@your-domain.example
SHINOX_ADMIN_TOKEN=long-random-secret-at-least-32-characters
SHINOX_FORM_LIVE=0
```

在受控主機的 Secret Manager / 環境變數設定，**不要把密碼貼進聊天或寫入 GitHub**。發件人必須是 SMTP 服務允許的寄件地址。預設使用 465/TLS；587/STARTTLS 亦支援。

```sh
python server.py --production --host 127.0.0.1 --port 3003 --db "$SHINOX_DB_PATH"
```

使用 HTTPS 反向代理將已確認網域的 `/` 導向本服務。後端預設只監聽 loopback，不要直接對公網暴露 Python 服務。正式主機需具備**不隨部署清除的資料磁碟**、進程自動重啟、HTTPS 憑證、備份、存取日誌及告警。部署前請核對合法個資告知與處理權利窗口。

## 驗收步驟

1. `python -m compileall -q server.py production_api.py tests`。
2. `python -m unittest discover -s tests -v`。這些測試使用虛構資料及 mock SMTP，**不代表真實 Email 已送達**。
3. 部署獨立、受限制的 HTTPS staging 網域和持久化磁碟，設定 SMTP 和管理金鑰；staging 才可暫設 `SHINOX_FORM_LIVE=1`。
4. 用**測試姓名、測試電話、測試 Email** 各送出一筆設備洽詢與展示洽詢，確認兩個指定信箱**都實際收到**含相同案件編號的通知；不得使用真實客戶資料。
5. 以管理金鑰進入 `/admin.html`，核對資料、狀態與 CSV；錯誤金鑰回傳 401、跨站來源回傳 403、無同意與格式錯誤回傳 400；確認前端失敗時不顯示成功。
6. 模擬 SMTP 中斷：資料必須仍存在，通知標記待寄送，恢復後成功補寄；驗證資料庫重啟後仍保留，備份可還原。
7. 確認行動版表單、中文與英文、個資告知、HTTPS、安全標頭、資料保存與刪除政策，並完成業主書面驗收。
8. **全部通過後**才在正式主機設 `SHINOX_FORM_LIVE=1`，重新檢查 `/api/status` 的 `acceptingLeads:true`，再實測正式網域。不可擅自替換既有正式網站或改變私人驗收站的存取權限。

## 尚待取得

- 正式網站託管／部署權限及 HTTPS 網域。
- 可持續運作的持久化資料庫磁碟與備份儲存。
- 寄信服務 SMTP 主機、已驗證寄件地址與安全保管的憑證。
- 業主核准的資料保存、個資告知、刪除流程與管理者名單。
- staging 真實寄信端到端測試證據，以及正式開放收件的最終核准。

未完成以上條件前，表單維持關閉。原本的電話、Email、WhatsApp 和 LINE 聯絡方式保持可用。
