"""
TCP socket server: accepts one connection, echoes each line back upper-cased.

Run standalone:
    python3 server.py
Then in another terminal:
    python3 client.py
"""
import socket

HOST = "127.0.0.1"
PORT = 50_007


def run_server() -> None:
    # SO_REUSEADDR lets us restart the server quickly without waiting out
    # the OS's TIME_WAIT period on the port.
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_sock:
        server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_sock.bind((HOST, PORT))
        server_sock.listen(1)
        print(f"[server] listening on {HOST}:{PORT}")

        conn, addr = server_sock.accept()
        with conn:
            print(f"[server] connection from {addr}")
            # TCP is a byte stream with no message boundaries, so we use a
            # buffered file-like wrapper to read line-by-line.
            reader = conn.makefile("r")
            writer = conn.makefile("w")
            for line in reader:
                line = line.rstrip("\n")
                if line == "QUIT":
                    break
                print(f"[server] received: {line!r}")
                writer.write(line.upper() + "\n")
                writer.flush()
        print("[server] connection closed")


if __name__ == "__main__":
    run_server()
