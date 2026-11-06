# ShinoX 隱私政策與表單資料流核對（2026-10-29）

## 可核實現況

- 私人驗收站使用 Sites 靜態託管及 ChatGPT 存取驗證；網站的 `api/status` 為 static-review、persistence:false、acceptingLeads:false、legalReviewAccepted:false。沒有在此部署 Python、SQLite 或 SMTP 收件服務。
- 網站品牌、電話及服務信箱可核實；實際營運公司或營運者名稱、個資權利負責窗口、正式儲存位置及服務商未確認。現有服務信箱可供提出問題，不把它冒稱為已核准的個資專責窗口。
- `server.py` / `production_api.py`：程式能力為私有 SQLite requests、通知 outbox、SMTP、Bearer 驗證之管理清單及 CSV；`scripts/backup_leads.py` 提供離線備份。它們不是已完成正式部署的證據。
- 程式目前資料庫清除設定30天；正式模式worker每60秒檢查，非正式模式啟動時檢查。此值尚未取得營運政策核准。Email副本、CSV與備份沒有自動跟隨資料庫清除，期限及刪除程序必須另行確認。
- 目前沒有 GA/GTM/Meta Pixel/廣告追蹤腳本、沒有應用程式自行設定的Cookie或localStorage。活動彈窗只用sessionStorage記錄看過狀態；託管與登入平台自身紀錄不在應用程式可核實範圍內。
- LINE/WhatsApp/Facebook/YouTube/Email/外部試算為外連。沒有自動傳送本站表單內容到這些平台；YouTube沒有內嵌自動播放器。

## 政策與路由

- 中文：`/privacy`、`/terms`；英文：`/en/privacy`、`/en/terms`。
- 原 `.html` 入口保留同內容。`build_legal_routes.py` 從同一份HTML產生目錄路由並正確改寫相對資源及頁面連結；本機靜態伺服器可導向帶斜線入口，不依賴特定平台重新導向設定。
- 中英文共用 `legal.css`、網站導覽、原LOGO及聯絡入口。全站頁尾有兩個法律連結。
- 更新日期2026-10-29，政策版本2026-10-29.1。政策描述目前停用狀態，未確認內容明列待確認；沒有虛構公司資料、保存承諾或安全認證。

## 收件及同意

- `legal-config.json` 的 reviewAccepted 為false，所有營運／保存核准欄位為null。
- 正式收件除了原有 `SHINOX_FORM_LIVE`、SMTP、資料庫條件，還必須通過政策完整資料與驗收閘門。只改live旗標或只改reviewAccepted都不能開放。
- 預覽伺服器預設也拒絕兩個POST收件路由；只有程式測試以明確測試參數使用隔離的合成資料。一般CLI沒有啟用該繞過參數。
- 兩種表單都保留未預選的必要確認欄，連結隱私權政策，資料用途限本次詢問，不包含行銷。因沒有行銷服務，沒有另建或預勾行銷選項。
- 瀏覽器只在勾選時於記憶體產生consentConfirmedAt，取消或重設即清空；送出時帶privacyPolicyVersion。沒有寫入Cookie或瀏覽器長期儲存。
- 後端驗證同意、政策版本與有時區的確認時間，儲存privacyPolicyVersion、consentVersion、瀏覽器回報consentConfirmedAt及獨立的UTC consentRecordedAt。案件created_at亦為伺服器時間。瀏覽器時間不是可信任伺服器時間。
- 未驗收時API在讀取表單內容及寫入資料庫前回503，不發Email。靜態託管則根本沒有收件API。

## 驗證及啟用限制

`python -m unittest discover -s tests -v` 使用合成資料及mock SMTP，驗證停用、版本及確認時間、資料持久化及通知功能；不代表已寄出真實Email。瀏覽器驗收以攔截方式模擬ready狀態，不會向真實收件服務提交資料。

待營運者確認名稱、權利窗口、資料庫／Email／備份期限與流程，完成政策及表單驗收、部署與真實端到端測試後，才可另行核准開放真實收件。本批只發布私人靜態驗收站。
