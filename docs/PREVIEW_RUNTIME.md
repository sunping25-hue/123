# ShinoX 本機預覽與表單資料

## 啟動

需要 Python 3.10 以上，無第三方相依套件：

```sh
python server.py --host 127.0.0.1 --port 3003
```

開啟 `http://127.0.0.1:3003`。若用執行環境的連接埠轉發，可使用 `--host 0.0.0.0`。這不會自動產生公開網址，也不部署正式站。

預設資料庫位於專案外 `../work/shinox-runtime/requests.sqlite3`，可用 `--db /path/to/private/requests.sqlite3` 指定。資料庫不應放入 `shinox-v2-site` 或 Git，檔案權限設為僅擁有者可讀寫。每次啟動會刪除超過 30 天的申請；長期運作需由正式主機排程落實保存期限及刪除權利。本機測試只使用虛構聯絡資料。

## 功能及限制

- 靜態網站及 MP4 HTTP byte ranges。
- `GET /api/status` 告知此服務為 `local-preview`。
- `POST /api/leads` 驗證姓名、至少一種聯絡方式及個資同意，寫入 SQLite。
- `POST /api/booking-requests` 額外接收希望地點、日期和時段；這只是洽詢，沒有可預約時段資料，也不代表預約成功。
- **未接正式寄信服務、業務通知或行事曆，不會寄信。** 回應明確包含 `emailSent:false` 與 `bookingConfirmed:false`。不提供公開查詢個資的 API。
- 同來源檢查、請求大小限制、每 IP 每十分鐘十次限制、蜜罐及伺服器端欄位驗證。

此執行程式只供本機驗收，不是正式客服系統。正式公開收件前，需接妥已授權的寄信與預約服務、完成個資告知/刪除窗口與保存政策、HTTPS、持久化備份、身分驗證管理介面及監控。未完成前請使用網站的電話或 Email 直接聯絡。

## API 契約

兩個 POST 路由均需 `Content-Type: application/json` 和與頁面相同的 `Origin`。反向代理應保留瀏覽器的 Host；若平台改寫 Host，僅設定已確認的預覽來源：

```sh
SHINOX_ALLOWED_ORIGINS=https://your-confirmed-preview.example python server.py
```

不預設信任任意 `X-Forwarded-Host` 或開啟跨來源收件。

共用 JSON 欄位：

```json
{
  "name": "測試姓名",
  "phone": "",
  "email": "preview@example.test",
  "region": "台南",
  "subject": "設備諮詢",
  "message": "純本機測試資料",
  "consent": true,
  "website": ""
}
```

`website` 是蜜罐，應留空。姓名必填，電話與 Email 至少一項，個資同意必須為布林值 `true`。展示洽詢可加 `location`、`preferredDate`（YYYY-MM-DD，不早於台灣當天日期）、`preferredTime`（希望時間說明，非已核可時段）。

寫入成功回傳 HTTP 201：

```json
{
  "ok": true,
  "requestId": "uuid",
  "status": "received_locally",
  "emailSent": false,
  "bookingConfirmed": false,
  "message": "詢問已儲存於本機預覽；尚未寄送或通知業務。請使用電話或 Email 完成聯絡。"
}
```

前端須直接說明回傳狀態，不得改寫為「通知已寄送」或「預約成功」。靜態主機沒有此 API，前端應保留電話/Email 備援，不能假裝送出。

## 驗證

```sh
python -m unittest discover -s tests -v
```

七項整合測試使用臨時檔案與虛構聯絡資料，涵蓋 SQLite 寫入、預約不誤報成功、驗證/同意、來源檢查、媒體 Range、私有資料不可查及限流。

## 路由、快取與保留期限

- 不存在的靜態頁面回傳真正 HTTP 404，並顯示網站的 `404.html`。本機伺服器會加入根路徑 `<base href="/">`，讓巢狀錯誤路徑上的 CSS、LOGO 和返回首頁連結仍能正常解析。API 404 維持 JSON。
- HTML、CSS、JavaScript 與圖片使用 `Cache-Control: no-cache`，讓每次預覽重新驗證檔案。MP4 使用 `private, max-age=300`；API 與錯誤頁使用 `no-store`。
- HEAD 與 GET 的 API 狀態一致，HEAD 不傳送內容；HEAD 媒體回應忽略 Range，描述整個檔案。GET 支援單一閉合、開放或後綴 byte range；無效範圍回傳 416。
- 隱私資料只存在本機 SQLite。**30 天清除是在伺服器每次啟動時執行，不是持續運行中的排程，也不保證準時於第 30 天清除。** `GET /api/status` 因此另回傳 `retentionPurge: "on_startup"`。驗收後應主動清除測試資料。

## 前端欄位長度上限

| 欄位 | 最多字元 |
|---|---:|
| name | 80 |
| phone | 30 |
| email | 254 |
| region | 100 |
| subject | 160 |
| message | 3000 |
| location（展示洽詢） | 160 |
| preferredDate（展示洽詢） | 10，必須為 YYYY-MM-DD |
| preferredTime（展示洽詢） | 100 |

姓名與個資同意必填；電話或 Email 至少提供一項。以上限制會在伺服器強制驗證，前端應使用相同上限。

目前十二項整合測試另涵蓋巢狀自訂 404、HEAD、查詢字串、錯誤/過大 Range、外部符號連結隔離、無效 Origin、靜態快取及真實啟動清除行為。
