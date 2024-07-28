import socket
import re

HOST = "localhost"
PORT = 4221


def main():
    server_socket = socket.create_server((HOST, PORT), reuse_port=True)
    conn, addr = server_socket.accept()  # wait for client

    data = conn.recv(2048)
    data_split = data.split(b"\r\n", maxsplit=1)

    response = "HTTP/1.1 200 OK\r\n\r\n"
    if data_split[0].split(b" ")[1] == b"/" or data_split[0].split(b" ")[1] == b"":
        conn.sendall(response.encode())
    else:
        request_target = data_split[0].split(b" ")[1]
        request_target_split = request_target.split(b"/")
        if request_target_split[1] == b"echo" and len(request_target_split) == 3:
            text = request_target_split[2].decode()
            content_length = str(len(text))
            response = ("HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: " + content_length
                        + "\r\n\r\n" + text)
            conn.sendall(response.encode())
        elif request_target == b"/user-agent":
            user_agent = re.search(r"User-Agent: ([\w./!@#$%^&*()+=-]*)", data_split[1].decode()).group()
            text = user_agent.split(" ")[1]
            content_length = str(len(text))
            response = ("HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: " + content_length
                        + "\r\n\r\n" + text)
            conn.sendall(response.encode())
        else:
            response = "HTTP/1.1 404 Not Found\r\n\r\n"
            conn.sendall(response.encode())


if __name__ == "__main__":
    main()
