#!/usr/bin/env python3
"""
Google Drive 完整測試腳本
"""

import json
from google.oauth2 import service_account
from googleapiclient.discovery import build

def main():
    service_account_file = '/home/ataya/.openclaw/media/inbound/spark-490715-a99b43f5f90c---61694565-2031-4efc-9c60-a2a99b477f49.json'
    SCOPES = ['https://www.googleapis.com/auth/drive']
    
    print("🔌 正在連接 Google Drive...")
    
    try:
        credentials = service_account.Credentials.from_service_account_file(
            service_account_file, scopes=SCOPES
        )
        
        print(f"✅ Service Account: {credentials.service_account_email}")
        
        service = build('drive', 'v3', credentials=credentials)
        
        # 查詢所有檔案
        print("\n📋 檔案列表 (最多 20 個):")
        print("-" * 60)
        
        request = service.files().list(
            spaces='drive',
            fields="files(id, name, mimeType, size, createdTime, modifiedTime, owners)"
        )
        
        response = request.execute()
        files = response.get('files', [])
        
        if files:
            print(f"找到 {len(files)} 個檔案:\n")
            for i, file in enumerate(files, 1):
                print(f"{i}. {file['name']}")
                print(f"   ID: {file['id']}")
                print(f"   類型：{file['mimeType']}")
                if file.get('size'):
                    size_mb = int(file['size']) / (1024 * 1024)
                    print(f"   大小：{size_mb:.2f} MB")
                print(f"   建立：{file['createdTime']}")
                print(f"   修改：{file['modifiedTime']}")
                if file.get('owners'):
                    owner = file['owners'][0].get('displayName', 'Unknown')
                    print(f"   擁有者：{owner}")
                print()
        else:
            print("   📭 Google Drive 根目錄是空的")
            print("\n✅ 連接成功！你可以開始上傳檔案或使用 API 操作了！")
        
        print("=" * 60)
        print("✅ 測試完成！Google Drive 連接正常！")
        
    except Exception as e:
        print(f"❌ 錯誤：{e}")

if __name__ == "__main__":
    main()
