# 基于 Socket 的视频传输系统

本项目实现了一个基于 Socket 的多客户端视频请求与实时解码播放系统，支持 TCP 网络传输、HM 解码器调用、YUV → RGB 转换、帧率控制与并发请求等功能。实现了以下功能：
- 多客户端并发请求服务端
- 视频片段顺序接收与连续播放
- YUV420 / YUV422 格式支持
- 支持动态调节播放速度（按 `+` / `-` 控制）
- 边解码边播放
## 📂 项目结构

```
client/                     # 客户端
├── ClientMain.py               # 客户端主程序
├── ThreadManager.py            # 控制接收+解码线程
├── Decoder/                    # 解码
│   ├── DecodePlayer.py             # 解码与播放脚本
│   └── TAppDecoder.exe             # HM 解码器（自行下载）
server/                     # 服务端
├── ServerMain.py               # 服务端主程序
├── ClientHandler.py                # 单个客户端请求处理逻辑
└── data/                           # 视频数据文件夹（3段×10片段）
```
## 🛠 环境依赖

- Python 3.10
- OpenCV
- Numpy


## ▶️ 使用方法

### 服务端启动：

```bash
cd server
python ServerMain.py
```

### 客户端启动：

```bash
cd client
python ClientMain.py
```

### 客户端运行中：
- 输入视频编号 
- 自动请求并播放全部片段
- 支持按 `+` 增加帧率，`-` 减少帧率，`q` 退出播放



## Reference

本项目使用 HEVC 参考解码器 TAppDecoder.exe.

官方仓库：https://vcgit.hhi.fraunhofer.de/jvet/HM

