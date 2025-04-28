import os
import threading
import subprocess


def run_client(video_id):
    subprocess.run(["python", "ClientMain.py", str(video_id)], cwd="client")


if __name__ == "__main__":
    thread_list = []
    client_num = 3

    for i in range(client_num):
        video_id = (i % 3) + 1  # 循环使用视频1~3
        t = threading.Thread(target=run_client, args=(video_id,))
        t.start()
        thread_list.append(t)

    # 等待所有线程结束
    for t in thread_list:
        t.join()

    print("[TEST DONE] 所有客户端模拟完成。")
