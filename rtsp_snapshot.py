#!/usr/bin/env python3
"""
RTSP 串流快照抓取工具
從 RTSP URL 抓取單張照片並存檔
"""

import cv2
import os
import sys
from datetime import datetime

def capture_rtsp_snapshot(rtsp_url, output_dir="./rtsp_snapshots", frame_number=None):
    """
    從 RTSP 串流抓取快照
    
    Args:
        rtsp_url: RTSP 串流 URL (例如: rtsp://username:password@192.168.1.100:554/stream)
        output_dir: 輸出目錄
        frame_number: 指定抓取哪一幀 (None 表示立即抓取)
    """
    
    # 創建輸出目錄
    os.makedirs(output_dir, exist_ok=True)
    
    # 創建時間戳文件名
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"rtsp_snapshot_{timestamp}.jpg"
    filepath = os.path.join(output_dir, filename)
    
    print(f"📹 連接到 RTSP: {rtsp_url}")
    
    # 創建 VideoCapture 對象
    cap = cv2.VideoCapture(rtsp_url, cv2.CAP_FFMPEG)
    
    # 設置超时時間 (毫秒) - 某些版本支援
    try:
        cap.set(cv2.CAP_PROP_FRAME_TIMEOUT, 5000)
    except AttributeError:
        print("⚠️  此版本 OpenCV 不支援 TIMEOUT 設置，將使用預設超時")
    
    if not cap.isOpened():
        print("❌ 無法連接到 RTSP 串流!")
        print("💡 檢查以下事項:")
        print("   - URL 格式是否正確")
        print("   - 網絡連線是否正常")
        print("   - 相機設備是否在線")
        print("   - 是否需要驗證憑證")
        return False
    
    # 如果指定了 frame_number，跳到該幀
    if frame_number is not None:
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
        print(f"⏭️ 跳到幀數: {frame_number}")
    
    # 讀取幀
    ret, frame = cap.read()
    
    if not ret:
        print("❌ 無法讀取畫面")
        cap.release()
        return False
    
    # 保存圖片
    if cv2.imwrite(filepath, frame):
        print(f"✅ 成功抓取快照！")
        print(f"📁 儲存位置：{os.path.abspath(filepath)}")
        print(f"📏 解析度：{frame.shape[1]}x{frame.shape[0]}")
    else:
        print("❌ 無法保存圖片")
    
    # 釋放資源
    cap.release()
    return True

def capture_continuous(rtsp_url, output_dir="./rtsp_snapshots", interval=5, duration=60):
    """
    連續抓取快照（每 interval 秒一張，持續 duration 秒）
    
    Args:
        rtsp_url: RTSP URL
        output_dir: 輸出目錄
        interval: 抓取間隔（秒）
        duration: 持續時間（秒）
    """
    
    print(f"🎬 連續抓取模式")
    print(f"📹 RTSP: {rtsp_url}")
    print(f"⏱️ 間隔：{interval} 秒")
    print(f"🕐 持續：{duration} 秒")
    
    capture_rtsp_snapshot(rtsp_url, output_dir)
    
    start_time = datetime.now()
    count = 0
    
    while True:
        # 檢查是否超過持續時間
        elapsed = (datetime.now() - start_time).total_seconds()
        if elapsed >= duration:
            print(f"\n⏰ 超過 {duration} 秒，停止抓取")
            break
        
        # 等待間隔
        import time
        time.sleep(interval)
        
        # 抓取
        count += 1
        print(f"\n⏱️ 抓取 #{count}")
        if not capture_rtsp_snapshot(rtsp_url, output_dir):
            print("❌ 連接失敗，停止抓取")
            break
    
    print(f"\n✅ 完成！共抓取 {count + 1} 張圖片")

if __name__ == "__main__":
    # 使用示例
    if len(sys.argv) < 2:
        print("用法:")
        print("  單張快照：python rtsp_snapshot.py <rtsp_url>")
        print("  連續抓取：python rtsp_snapshot.py <rtsp_url> --continuous --interval 5 --duration 60")
        print()
        print("範例:")
        print("  python rtsp_snapshot.py \"rtsp://admin:password@192.168.1.100:554/stream1\"")
        print("  python rtsp_snapshot.py \"rtsp://user:pass@10.0.0.1:554/axis-media/media.amp?videocodec=h264\" --continuous --interval 10 --duration 120")
        sys.exit(1)
    
    rtsp_url = sys.argv[1]
    
    # 檢查參數
    continuous = "--continuous" in sys.argv
    interval = 5
    duration = 60
    
    if "--interval" in sys.argv:
        idx = sys.argv.index("--interval")
        if idx + 1 < len(sys.argv):
            interval = int(sys.argv[idx + 1])
    
    if "--duration" in sys.argv:
        idx = sys.argv.index("--duration")
        if idx + 1 < len(sys.argv):
            duration = int(sys.argv[idx + 1])
    
    if continuous:
        capture_continuous(rtsp_url, interval=interval, duration=duration)
    else:
        capture_rtsp_snapshot(rtsp_url)
