import socket

HOST = "localhost"
PORT = 4221


def main():
    server_socket = socket.create_server((HOST, PORT), reuse_port=True)
    conn, addr = server_socket.accept()  # wait for client
    response_msg = "HTTP/1.1 200 OK\r\n\r\n"
    conn.sendall(__data=response_msg.encode())


if __name__ == "__main__":
    main()
