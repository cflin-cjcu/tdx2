"""
TDX API 服務模組
處理 TDX API 認證和資料取得
"""

import requests
from datetime import datetime, timedelta
from config import CONFIG


class TDXService:
    """TDX API 服務類別"""
    
    def __init__(self):
        self.client_id = CONFIG['client_id']
        self.client_secret = CONFIG['client_secret']
        self.auth_url = CONFIG['auth_url']
        self.api_url = CONFIG['api_url']
        
        # Token 快取
        self.access_token = None
        self.token_expires_at = None
    
    def get_access_token(self):
        """
        取得 Access Token (實作快取機制)
        
        Returns:
            str: Access Token
        """
        # 檢查是否有快取的 Token 且未過期 (提前 5 分鐘更新)
        if self.access_token and self.token_expires_at:
            if datetime.now() < self.token_expires_at - timedelta(minutes=5):
                print(f"使用快取的 Access Token (有效期至: {self.token_expires_at})")
                return self.access_token
        
        # 取得新的 Token
        print("正在取得新的 Access Token...")
        
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        
        data = {
            'grant_type': 'client_credentials',
            'client_id': self.client_id,
            'client_secret': self.client_secret
        }
        
        try:
            response = requests.post(self.auth_url, headers=headers, data=data)
            response.raise_for_status()
            
            result = response.json()
            self.access_token = result['access_token']
            expires_in = result.get('expires_in', 86400)  # 預設 1 天
            
            self.token_expires_at = datetime.now() + timedelta(seconds=expires_in)
            
            print(f"✓ Access Token 取得成功 (有效期: {expires_in} 秒)")
            return self.access_token
            
        except requests.exceptions.RequestException as e:
            print(f"✗ 取得 Access Token 失敗: {e}")
            raise
    
    def get_train_live_board(self):
        """
        取得台鐵列車即時動態資料
        
        Returns:
            list: 列車動態資料列表
        """
        try:
            token = self.get_access_token()
            
            headers = {
                'Authorization': f'Bearer {token}'
            }
            
            print("正在取得台鐵列車即時動態資料...")
            response = requests.get(self.api_url, headers=headers)
            
            # 如果是 401 錯誤，清除 Token 快取並重試
            if response.status_code == 401:
                print("Token 已失效，重新取得...")
                self.access_token = None
                self.token_expires_at = None
                token = self.get_access_token()
                headers['Authorization'] = f'Bearer {token}'
                response = requests.get(self.api_url, headers=headers)
            
            response.raise_for_status()
            data = response.json()
            
            trains = data.get('TrainLiveBoards', [])
            print(f"✓ 成功取得 {len(trains)} 筆列車資料")
            
            return trains
            
        except requests.exceptions.RequestException as e:
            print(f"✗ 取得列車資料失敗: {e}")
            raise


# 全域服務實例
tdx_service = TDXService()


def get_train_data():
    """
    取得並格式化列車資料
    
    Returns:
        list: 格式化的列車資料
    """
    trains = tdx_service.get_train_live_board()
    
    formatted_data = []
    for idx, train in enumerate(trains, 1):
        # 處理列車類型 - 可能是字串或字典
        train_type_name = train.get('TrainTypeName', 'N/A')
        if isinstance(train_type_name, dict):
            train_type_name = train_type_name.get('zh-tw', train_type_name.get('Zh_tw', 'N/A'))
        
        # 處理站名 - 可能是字串或字典
        station_name = train.get('StationName', 'N/A')
        if isinstance(station_name, dict):
            station_name = station_name.get('zh-tw', station_name.get('Zh_tw', 'N/A'))
        
        formatted_data.append({
            '序號': idx,
            '車次': train.get('TrainNo', 'N/A'),
            '列車類型': train_type_name if train_type_name else 'N/A',
            '即將到達': station_name if station_name else 'N/A',
            '延遲時間': train.get('DelayTime', 0),
            '更新時間': train.get('UpdateTime', 'N/A')
        })
    
    return formatted_data
