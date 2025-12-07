# 台鐵列車即時動態資訊系統 (Python)

這是一個使用 Python 和 TDX (Transport Data eXchange) API 建立的台鐵列車即時動態資訊系統，提供兩種不同的前端實作版本。

## 🎯 功能特色

- ✅ 自動取得並管理 TDX Access Token (實作快取機制)
- ✅ 即時顯示台鐵列車動態資料
- ✅ 延遲時間長條圖視覺化
- ✅ 延遲時間色彩標示 (準點/輕微/中度/嚴重)
- ✅ 顯示列車詳細資訊 (車次、類型、即將到達站、延遲時間)
- ✅ 自動每 30 秒更新資料
- ✅ 手動重新整理功能
- ✅ 響應式設計，適配各種螢幕尺寸
- ✅ 設定檔分離，保護敏感資訊

## 📦 兩種版本

### 版本 1: Plotly Dash 版 (`app.py`)

**技術架構**:
- **後端**: Python 3.x
- **前端框架**: Plotly Dash + Dash Bootstrap Components
- **圖表**: Plotly
- **資料處理**: Pandas
- **HTTP 請求**: Requests

**特色**:
- 整合式 Python 框架
- 內建表格排序、篩選、分頁功能
- 快速開發，代碼簡潔

### 版本 2: PyEcharts 版 (`app1.py`)

**技術架構**:
- **後端**: Flask
- **前端**: 自訂 HTML/CSS/JavaScript
- **圖表**: ECharts (通過 PyEcharts)
- **資料處理**: Pandas
- **HTTP 請求**: Requests

**特色**:
- RESTful API 架構
- 美觀的漸層視覺設計
- 豐富的圖表互動效果
- 完全自訂的 UI/UX

## 📁 檔案結構

```
tdx2/
├── app.py              # 主應用程式 (Plotly Dash 版本)
├── app1.py             # 主應用程式 (PyEcharts 版本)
├── tdx_service.py      # TDX API 服務模組
├── config.py           # API 設定檔 (包含敏感資訊，不應提交至 Git)
├── config.example.py   # 設定檔範例
├── requirements.txt    # Python 套件相依性
├── .gitignore          # Git 忽略清單
└── README.md           # 說明文件
```

## 安裝與設定

### 1. 環境需求

- Python 3.8 或更高版本
- pip (Python 套件管理工具)

### 2. 取得 TDX API 憑證

1. 前往 [TDX 運輸資料流通服務平台](https://tdx.transportdata.tw/)
2. 註冊並登入帳號
3. 進入「會員中心」取得 Client ID 和 Client Secret

### 3. 安裝相依套件

```powershell
# 安裝所需套件
pip install -r requirements.txt
```

### 4. 設定 API 憑證

複製 `config.example.py` 並重新命名為 `config.py`：

```powershell
Copy-Item config.example.py config.py
```

編輯 `config.py`，填入您的 API 憑證：

```python
CONFIG = {
    'client_id': '您的_CLIENT_ID',
    'client_secret': '您的_CLIENT_SECRET',
    'auth_url': 'https://tdx.transportdata.tw/auth/realms/TDXConnect/protocol/openid-connect/token',
    'api_url': 'https://tdx.transportdata.tw/api/basic/v3/Rail/TRA/TrainLiveBoard?$top=60&$format=JSON'
}
```

### 5. 執行應用程式

**選擇版本 1 (Plotly Dash)**：
```powershell
python app.py
```
然後在瀏覽器開啟 `http://127.0.0.1:8050`

**選擇版本 2 (PyEcharts + Flask)**：
```powershell
python app1.py
```
然後在瀏覽器開啟 `http://127.0.0.1:5000`

## 📊 使用方式

### 查看即時資料

- 頁面載入後會自動取得台鐵列車即時動態資料
- 資料每 30 秒自動更新
- 可點擊「🔄 重新整理」按鈕手動更新

### 版本差異

| 功能 | Plotly Dash 版 (app.py) | PyEcharts 版 (app1.py) |
|------|------------------------|----------------------|
| 執行端口 | http://127.0.0.1:8050 | http://127.0.0.1:5000 |
| 圖表庫 | Plotly | ECharts |
| 表格功能 | 排序、篩選、分頁 | 基本表格 |
| 視覺設計 | Bootstrap 主題 | 自訂漸層設計 |
| 開發難度 | 簡單 (純 Python) | 中等 (需 HTML/JS) |
| 圖表互動 | 標準 Plotly 互動 | 豐富的懸停提示 |
| API 架構 | 內建 Callback | RESTful API |

### 表格功能 (Plotly Dash 版專屬)

- **排序**: 點擊欄位標題可進行排序
- **篩選**: 每個欄位下方可輸入篩選條件
- **分頁**: 每頁顯示 20 筆資料，可切換頁面

### 資料說明

頁面會顯示最多 60 筆列車資料，包含：

| 欄位     | 說明                                        |
| -------- | ------------------------------------------- |
| 序號     | 資料編號                                    |
| 車次     | 列車編號 (TrainNo)                          |
| 列車類型 | 車次類型，如:自強號、莒光號 (TrainTypeName) |
| 即將到達 | 列車即將到達的站名 (StationName)            |
| 延遲時間 | 列車延遲分鐘數 (DelayTime)                  |
| 更新時間 | 資料最後更新時間 (UpdateTime)               |

### 延遲狀態標示

- 🟢 **準點** (0 分鐘) - 綠色背景
- 🟡 **輕微延遲** (1-5 分鐘) - 黃色背景
- 🟠 **中度延遲** (6-10 分鐘) - 橘色背景
- 🔴 **嚴重延遲** (>10 分鐘) - 紅色背景

## 🔧 模組說明

### tdx_service.py

TDX API 服務模組，提供：

- `TDXService` 類別：處理 API 認證和資料取得
  - `get_access_token()`: 取得並快取 Access Token
  - `get_train_live_board()`: 取得列車即時動態資料
- `get_train_data()`: 取得並格式化列車資料

**Token 快取機制**:
1. Token 儲存在記憶體中
2. 記錄 Token 過期時間 (預設 1 天)
3. 每次呼叫前檢查 Token 是否有效
4. Token 過期前 5 分鐘自動重新取得
5. 若 API 回傳 401，自動清除並重新取得 Token

### app.py (Plotly Dash 版)

使用 Plotly Dash 建立前端介面：

- 使用 Dash Bootstrap Components 美化介面
- 實作自動更新機制 (每 30 秒)
- 提供手動更新按鈕
- 根據延遲時間動態設定儲存格樣式
- 提供排序、篩選、分頁功能
- 整合 Plotly 長條圖顯示延遲時間

### app1.py (PyEcharts 版)

使用 Flask + ECharts 建立前端介面：

- Flask RESTful API 架構
- 自訂 HTML/CSS 美化介面
- ECharts 互動式長條圖
- 漸層視覺設計
- 豐富的懸停提示資訊
- 自動更新機制 (每 30 秒)

## API 說明

### TDX API 端點

- **驗證 API**: `https://tdx.transportdata.tw/auth/realms/TDXConnect/protocol/openid-connect/token`
- **列車動態 API**: `https://tdx.transportdata.tw/api/basic/v3/Rail/TRA/TrainLiveBoard`

### 參數說明

- `$top=60`: 取得最多 60 筆資料
- `$format=JSON`: 回傳 JSON 格式

## 錯誤處理

- 若無法取得 API 憑證，會顯示錯誤訊息
- 若 Token 過期，會自動重新取得
- 若資料取得失敗，會顯示錯誤警告
- 所有錯誤都會在控制台輸出詳細資訊

## 🎨 開發建議

### 自訂更新頻率

**Plotly Dash 版 (app.py)**：
修改 `dcc.Interval` 組件：
```python
dcc.Interval(
    id='interval-component',
    interval=30*1000,  # 改為您想要的秒數 * 1000
    n_intervals=0
)
```

**PyEcharts 版 (app1.py)**：
修改 JavaScript 中的定時器：
```javascript
// 每 30 秒自動更新
autoRefreshInterval = setInterval(refreshData, 30000);  // 改為您想要的毫秒數
```

### 調整資料筆數

修改 `config.py` 中的 API URL：
```python
'api_url': 'https://tdx.transportdata.tw/api/basic/v3/Rail/TRA/TrainLiveBoard?$top=100&$format=JSON'  # 改為 100 筆
```

### 自訂樣式

**Plotly Dash 版**：
修改 `app.py` 中的 `style_header`、`style_cell` 等參數來調整表格樣式。

**PyEcharts 版**：
修改 `app1.py` 中 HTML_TEMPLATE 的 CSS 樣式，或調整 ECharts 的 option 配置。

## 💡 版本選擇建議

### 選擇 Plotly Dash 版 (app.py) 如果您：
- ✅ 想要快速開發，減少 HTML/JavaScript 代碼
- ✅ 需要強大的表格功能（排序、篩選、分頁）
- ✅ 偏好 Python 原生的開發體驗
- ✅ 需要更多 Plotly 的內建圖表類型

### 選擇 PyEcharts 版 (app1.py) 如果您：
- ✅ 需要完全自訂的 UI/UX 設計
- ✅ 想要 RESTful API 架構
- ✅ 偏好 ECharts 的視覺效果和互動性
- ✅ 需要將 API 整合到其他前端應用

## ⚠️ 注意事項

1. **請勿將 `config.py` 提交至 Git**，以保護您的 API 憑證
2. TDX API 有使用限制，請適度調整更新頻率
3. 確保網路連線正常，以順利取得資料
4. 建議在穩定的 Python 環境中執行
5. 兩個版本 (`app.py` 和 `app1.py`) 使用不同端口，可以同時執行

## 🚀 快速開始指令

```powershell
# 1. 安裝套件
pip install -r requirements.txt

# 2. 設定 API 憑證
Copy-Item config.example.py config.py
# 然後編輯 config.py 填入您的憑證

# 3. 執行 Plotly Dash 版
python app.py
# 開啟 http://127.0.0.1:8050

# 或執行 PyEcharts 版
python app1.py
# 開啟 http://127.0.0.1:5000
```

## 授權

此專案僅供學習和個人使用。TDX API 資料版權屬於交通部。

## 📚 參考資源

- [TDX 運輸資料流通服務](https://tdx.transportdata.tw/)
- [Plotly Dash 官方文件](https://dash.plotly.com/)
- [Dash Bootstrap Components](https://dash-bootstrap-components.opensource.faculty.ai/)
- [PyEcharts 官方文件](https://pyecharts.org/)
- [ECharts 官方文件](https://echarts.apache.org/)
- [Flask 官方文件](https://flask.palletsprojects.com/)

## 📸 功能截圖

### Plotly Dash 版特色
- 整合式表格（排序、篩選、分頁）
- Plotly 互動式長條圖
- Bootstrap 清爽介面
- 延遲時間色彩標示

### PyEcharts 版特色
- 漸層視覺設計
- ECharts 豐富圖表互動
- 自訂 HTML/CSS 介面
- RESTful API 架構

## 🔄 更新日誌

### v2.0 (2025-12-07)
- ✨ 新增 PyEcharts 版本 (app1.py)
- ✨ 新增延遲時間長條圖 (兩個版本)
- 🐛 修正列車類型顯示問題
- 📝 更新 README 說明

### v1.0 (2025-12-04)
- 🎉 初始版本發布
- ✅ Plotly Dash 版本
- ✅ TDX API 整合
- ✅ Token 快取機制
- ✅ 自動更新功能

## 👨‍💻 聯絡資訊

如有問題或建議，歡迎提出 Issue 或 Pull Request。
