"""
TDX API 設定檔範例
請複製此檔案為 config.py 並填入您的 API 憑證
"""

CONFIG = {
    'client_id': '您的_CLIENT_ID',
    'client_secret': '您的_CLIENT_SECRET',
    'auth_url': 'https://tdx.transportdata.tw/auth/realms/TDXConnect/protocol/openid-connect/token',
    'api_url': 'https://tdx.transportdata.tw/api/basic/v3/Rail/TRA/TrainLiveBoard?$top=60&$format=JSON'
}
