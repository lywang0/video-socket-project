import os


def handle_client(client_socket):
    try:
        request = client_socket.recv(1024).decode()
        video_id, segment_id = request.strip().split()
        # print(video_id, segment_id)
        filename = f"data/video{video_id}/{segment_id}.bin"
        # print(filename)
        if not os.path.exists(filename):
            client_socket.send(b"[ERROR] File not found")
            return

        with open(filename, "rb") as f:
            data = f.read()
            client_socket.sendall(data)
            print(f"[INFO] {filename} has been sent")

    except Exception as e:
        print(f"[ERROR] {e}")

    finally:
        client_socket.close()


