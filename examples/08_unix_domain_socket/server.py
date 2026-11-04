"""
Unix domain socket server: accepts one connection, echoes each line back
reversed.

Run standalone:
    python3 server.py
Then in another terminal:
    python3 client.py
"""
import os
import socket

SOCKET_PATH = "/tmp/ipc-demo.sock"


def run_server() -> None:
    # Remove a stale socket file from a previous run, if present.
    if os.path.exists(SOCKET_PATH):
        os.unlink(SOCKET_PATH)

    with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as server_sock:
        server_sock.bind(SOCKET_PATH)
        server_sock.listen(1)
        print(f"[server] listening on {SOCKET_PATH}")

        conn, _ = server_sock.accept()
        with conn:
            reader = conn.makefile("r")
            writer = conn.makefile("w")
            for line in reader:
                line = line.rstrip("\n")
                if line == "QUIT":
                    break
                print(f"[server] received: {line!r}")
                writer.write(line[::-1] + "\n")
                writer.flush()
    os.unlink(SOCKET_PATH)  # clean up the socket file
    print("[server] stopped")


if __name__ == "__main__":
    run_server()
