import socket, os
from Decoder.DecodePlayer import decode_and_play

SERVER_IP = '127.0.0.1'
PORT = 8001

def request_segment(video_id, segment_id):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((SERVER_IP, PORT))

    request = f"{video_id} {segment_id}"
    client_socket.send(request.encode())

    filename = f"received/video{video_id}/{segment_id}.bin"
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, "wb") as f:
        while chunk := client_socket.recv(4096):
            f.write(chunk)

    client_socket.close()
    return filename  # 返回下载路径给统一播放函数用

if __name__ == "__main__":
    video_id = input("请输入要播放的视频编号（1/2/3）:").strip()
    if video_id not in ["1", "2", "3"]:
        print("[ERROR] 无效的视频编号，请输入 1、2 或 3")
    else:
        segment_paths = []
        for segment_id in range(1, 11):
            path = request_segment(video_id, segment_id)
            segment_paths.append((path, video_id, segment_id))

        decode_and_play(segment_paths)
