import socket
import re
import threading
import sys

HOST = "localhost"
PORT = 4221


def handle(conn, addr):
    data = conn.recv(2048)
    data_split = data.split(b"\r\n", maxsplit=1)

    response = "HTTP/1.1 200 OK\r\n\r\n"
    if data_split[0].split(b" ")[1] == b"/" or data_split[0].split(b" ")[1] == b"":
        conn.sendall(response.encode())
    else:
        request_target = data_split[0].split(b" ")[1]
        request_target_split = request_target.split(b"/")
        if request_target_split[1] == b"echo" and len(request_target_split) == 3:
            # Here we just extract the string from /echo/{str} request target
            # after which we respond with that same {str} as a body message
            text = request_target_split[2].decode()
            content_length = str(len(text))
            response = ("HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: " + content_length
                        + "\r\n\r\n" + text)
            conn.sendall(response.encode())
        elif request_target == b"/user-agent":
            # I used regex here to search for User-Agent literal string in case there would be more
            # headers
            user_agent = re.search(r"User-Agent: ([\w./!@#$%^&*()+=-]*)", data_split[1].decode()).group()
            text = user_agent.split(" ")[1]
            content_length = str(len(text))
            response = ("HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: " + content_length
                        + "\r\n\r\n" + text)
            conn.sendall(response.encode())
        elif request_target_split[1] == b"files":
            dir_name = sys.argv[2]
            file_name = request_target[7:]
            try:
                with open(f"/{dir_name}/{file_name}", "rb") as file:
                    content = file.read()
                    content_length = str(len(content))
                    response = (f"HTTP/1.1 200 OK\r\nContent-Type: application/octet-stream\r\nContent-Length:"
                                f" {content_length}\r\n\r\n{content}")
            except FileNotFoundError as e:
                response = "HTTP/1.1 404 Not Found\r\n\r\n"
            finally:
                conn.sendall(response.encode())
        else:
            response = "HTTP/1.1 404 Not Found\r\n\r\n"
            conn.sendall(response.encode())


def main():
    server_socket = socket.create_server((HOST, PORT), reuse_port=True)
    while True:
        conn, addr = server_socket.accept()  # wait for client
        # handle(conn, addr)
        threading.Thread(target=handle, args=(conn, addr)).start()


if __name__ == "__main__":
    main()
