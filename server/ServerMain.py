import socket
import threading
from ClientHandler import handle_client

HOST = '0.0.0.0'
PORT = 8001


def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen()
    print(f'[INFO] server is listening on {HOST}:{PORT}')

    while True:
        client_socket, addr = server_socket.accept()
        print(f'[INFO] client is connected {addr}')
        thread = threading.Thread(target=handle_client, args=(client_socket,))
        thread.daemon = True  # 守护线程防止死锁
        thread.start()


if __name__ == '__main__':
    main()
