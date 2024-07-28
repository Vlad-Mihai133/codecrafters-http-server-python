import socket

HOST = "localhost"
PORT = 4221


def main():
    server_socket = socket.create_server((HOST, PORT), reuse_port=True)
    conn, addr = server_socket.accept()  # wait for client

    data = conn.recv(2048)
    data_split = data.split(b"\r\n")

    response = "HTTP/1.1 200 OK\r\n\r\n"
    if data_split[0].split(b" ")[1] == b"/" or data_split[0].split(b" ")[1] == b"":
        conn.sendall(response.encode())
    else:
        response = "HTTP/1.1 404 Not Found\r\n\r\n"
        conn.sendall(response.encode())


if __name__ == "__main__":
    main()
