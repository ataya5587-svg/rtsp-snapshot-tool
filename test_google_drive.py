#!/usr/bin/env python3
"""
Google Drive 連接測試腳本
測試 Service Account 是否可以存取 Google Drive
"""

import json
import sys
from google.oauth2 import service_account
from googleapiclient.discovery import build

def test_google_drive():
    """測試 Google Drive 連接"""
    
    # Service Account JSON 路徑
    service_account_file = '/home/ataya/.openclaw/media/inbound/spark-490715-a99b43f5f90c---61694565-2031-4efc-9c60-a2a99b477f49.json'
    
    # 權限範圍
    SCOPES = ['https://www.googleapis.com/auth/drive']
    
    print("🔌 正在連接 Google Drive...")
    print(f"📁 Service Account 檔案：{service_account_file}")
    print()
    
    try:
        # 載入 Service Account 憑證
        with open(service_account_file, 'r') as f:
            credentials = service_account.Credentials.from_service_account_file(
                service_account_file,
                scopes=SCOPES
            )
        
        print(f"✅ Service Account 載入成功")
        print(f"   Client Email: {credentials.service_account_email}")
        print(f"   權限範圍：{credentials.scopes}")
        print()
        
        # 建立 Drive API 服務
        service = build('drive', 'v3', credentials=credentials)
        print("✅ Drive API 服務建立成功")
        print()
        
        # 測試 1: 列出根目錄檔案
        print("📋 測試 1: 列出根目錄檔案")
        print("-" * 50)
        
        page_token = None
        results = []
        while True:
            results_request = service.files().list(
                spaces='drive',
                fields="nextPageToken, files(id, name, mimeType, size, createdTime, modifiedTime)",
                pageToken=page_token
            )
            results = results_request.execute()
            files = results.get('files', [])
            
            if files:
                for file in files:
                    print(f"   📄 {file['name']}")
                    print(f"      ID: {file['id']}")
                    print(f"      類型：{file['mimeType']}")
                    if file.get('size'):
                        size = int(file['size']) / (1024 * 1024)
                        print(f"      大小：{size:.2f} MB")
                    print(f"      建立時間：{file['createdTime']}")
                    print(f"      修改時間：{file['modifiedTime']}")
                    print()
            else:
                print("   📭 根目錄是空的")
                print()
            
            page_token = results.get('nextPageToken')
            if not page_token:
                break
        
        # 測試 2: 查詢我的檔案
        print("📋 測試 2: 查詢所有檔案")
        print("-" * 50)
        query = "trashed = false"
        response = service.files().list(
            q=query,
            spaces='drive',
            fields="files(id, name, mimeType, size, parents)",
            maxResults=10
        ).execute()
        
        files = response.get('files', [])
        print(f"   找到 {len(files)} 個檔案（最多顯示 10 個）:")
        print()
        
        for i, file in enumerate(files, 1):
            print(f"   {i}. {file['name']}")
            print(f"      類型：{file['mimeType']}")
            if file.get('size'):
                size = int(file['size']) / (1024 * 1024)
                print(f"      大小：{size:.2f} MB")
            if file.get('parents'):
                print(f"      父目錄 ID: {file['parents'][0]}")
            print()
        
        print("✅ 所有測試完成！Google Drive 連接成功！")
        return True
        
    except FileNotFoundError:
        print(f"❌ 錯誤：找不到 Service Account 檔案：{service_account_file}")
        return False
    except ImportError as e:
        print(f"❌ 錯誤：缺少 Python 套件 - {e}")
        print("請先安裝：pip install google-api-python-client google-auth-httplib2")
        return False
    except Exception as e:
        print(f"❌ 錯誤：{e}")
        return False

if __name__ == "__main__":
    success = test_google_drive()
    sys.exit(0 if success else 1)
