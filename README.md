# RTSP Camera Snapshot Tool

一個使用 Python 和 OpenCV 從 RTSP 串流抓取快照的自動化工具。

## 📋 功能特點

- ✅ 從 RTSP URL 抓取單張靜態畫面
- ✅ 連續抓取模式（可設定間隔和持續時間）
- ✅ 自動儲存為 JPG 格式
- ✅ 支援指定幀數抓取
- ✅ 清晰的錯誤提示和狀態信息

## 🚀 快速開始

### 1. 安裝依賴

```bash
pip install opencv-python
```

### 2. 使用方式

#### 抓取單張快照
```bash
python3 rtsp_snapshot.py "rtsp://username:password@192.168.1.100:554/stream"
```

#### 連續抓取（每 5 秒 1 張，持續 60 秒）
```bash
python3 rtsp_snapshot.py "rtsp://username:password@192.168.1.100:554/stream" --continuous --interval 5 --duration 60
```

### 3. 輸出

- 預設輸出目錄：`./rtsp_snapshots/`
- 檔案格式：`rtsp_snapshot_YYYYMMDD_HHMMSS.jpg`
- 解析度：原始串流解析度

## 🔧 常見 RTSP URL 格式

- **Hikvision:** `rtsp://admin:password@192.168.1.100:554/Streaming/Channels/101`
- **Dahua:** `rtsp://admin:password@192.168.1.100:554/cam/realmonitor?channel=1&subtype=0`
- **Axis:** `rtsp://user:pass@10.0.0.1:554/axis-media/media.amp?videocodec=h264`
- **Generic:** `rtsp://username:password@IP:554/stream`

## 📝 參數說明

```
--continuous      連續抓取模式
--interval N      抓取間隔（秒），預設 5 秒
--duration N      持續時間（秒），預設 60 秒
```

## 📦 依賴

- Python 3.x
- opencv-python
- numpy

## 📄 授權

MIT License

## 🔗 相關資源

- [OpenCV 官方文檔](https://docs.opencv.org/)
- [RTSP 協定](https://en.wikipedia.org/wiki/Real_Time_Streaming_Protocol)
