import os
import numpy as np
import cv2
import time
import threading
from queue import Queue

VIDEO_INFO = {
    '1': {"format": "YUV420", "width": 832, "height": 480},
    '2': {"format": "YUV420", "width": 960, "height": 540},
    '3': {"format": "YUV422", "width": 800, "height": 480},
}

PLAYBACK_FPS = 60  # 默认视频播放帧率

frame_queue = Queue()
exit_signal = object()

def decode_segment(bin_path, video_id, segment_id):
    """
    解码视频片段的二进制码流，并将每帧 YUV 数据放入播放队列。
    """
    yuv_path = f"decoded/video{video_id}/{segment_id}.yuv"
    os.makedirs(os.path.dirname(yuv_path), exist_ok=True)

    input_path = os.path.join(".\\", bin_path)
    output_path = os.path.join(".\\", yuv_path)
    os.system(f"Decoder\\TAppDecoder.exe -b {input_path} -o {output_path}")
    print(f"[INFO] Decoded to {yuv_path}")

    info = VIDEO_INFO[str(video_id)]
    width, height = info["width"], info["height"]
    fmt = info["format"]

    with open(yuv_path, "rb") as f:
        yuv_data = f.read()

    if fmt == "YUV420":
        frame_size = int(height * 1.5) * width
        frame_count = len(yuv_data) // frame_size
        for i in range(frame_count):
            frame = np.frombuffer(
                yuv_data[i * frame_size:(i + 1) * frame_size],
                dtype=np.uint8
            ).reshape((int(height * 1.5), width))
            frame_queue.put(("YUV420", frame, width, height))

    elif fmt == "YUV422":
        frame_size = width * height
        uv_size = frame_size // 2   # U 和 V 分量总共为 Y 的一半（4:2:2）
        frame_count = len(yuv_data) // (frame_size + uv_size * 2)  # 每帧所需字节数

        for i in range(frame_count):
            base = i * (frame_size + 2 * uv_size)  # 当前帧在字节流中的起始位置

            # 提取 Y,U,V 分量并 reshape 为二维图像
            y = np.frombuffer(yuv_data[base: base + frame_size], dtype=np.uint8).reshape((height, width))
            u = np.frombuffer(yuv_data[base + frame_size: base + frame_size + uv_size], dtype=np.uint8).reshape(
                (height, width // 2))
            v = np.frombuffer(yuv_data[base + frame_size + uv_size: base + frame_size + 2 * uv_size], dtype=np.uint8).reshape(
                (height, width // 2))

            # 将 U/V 分量上采样回原始图像尺寸
            u_up = cv2.resize(u, (width, height), interpolation=cv2.INTER_LINEAR)
            v_up = cv2.resize(v, (width, height), interpolation=cv2.INTER_LINEAR)

            # 合并 YUV 三通道并送入播放队列
            yuv = cv2.merge([y, u_up, v_up])
            frame_queue.put(("YUV_PLANAR_422", yuv, width, height))

def player_loop():
    """
    播放线程主循环，从帧队列中取出图像帧，控制播放速率并显示。
    """
    global PLAYBACK_FPS
    frame_interval = 1.0 / PLAYBACK_FPS
    last_frame_time = time.time()

    print("[INFO] 按 [+] 加快播放，[-] 减慢播放，按 [q] 退出。")

    while True:
        item = frame_queue.get()
        if item is exit_signal:
            break

        fmt, frame, width, height = item

        if fmt == "YUV420":
            bgr = cv2.cvtColor(frame, cv2.COLOR_YUV2BGR_I420)
        elif fmt == "YUV_PLANAR_422":
            bgr = cv2.cvtColor(frame, cv2.COLOR_YUV2BGR)
        else:
            continue

        # 时间控制播放
        now = time.time()
        elapsed = now - last_frame_time
        if elapsed < frame_interval:
            time.sleep(frame_interval - elapsed)
        last_frame_time = time.time()

        cv2.imshow("Video Play", bgr)
        key = cv2.waitKey(1) & 0xFF

        if key == ord('q'):
            break
        elif key == ord('+') or key == ord('='):  # 支持=和+
            PLAYBACK_FPS = min(120, PLAYBACK_FPS + 5)
            print(f"[INFO] 播放帧率增加到 {PLAYBACK_FPS} FPS")
        elif key == ord('-') or key == ord('_'):
            PLAYBACK_FPS = max(5, PLAYBACK_FPS - 5)
            print(f"[INFO] 播放帧率降低到 {PLAYBACK_FPS} FPS")

        # 实时更新间隔
        frame_interval = 1.0 / PLAYBACK_FPS

    cv2.destroyAllWindows()

def decode_and_play(segments):
    """
    主入口：接收视频片段路径，开启播放线程并顺序解码播放。
    """
    player = threading.Thread(target=player_loop)
    player.start()

    for bin_path, video_id, segment_id in segments:
        decode_segment(bin_path, video_id, segment_id)

    frame_queue.put(exit_signal)
    player.join()


