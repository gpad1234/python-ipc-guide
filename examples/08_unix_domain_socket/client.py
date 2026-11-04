"""
Unix domain socket client: connects to server.py, sends a few lines,
prints the reversed echoes.

Run standalone (after starting server.py in another terminal):
    python3 client.py
"""
import socket

SOCKET_PATH = "/tmp/ipc-demo.sock"


def run_client() -> None:
    with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as sock:
        sock.connect(SOCKET_PATH)
        reader = sock.makefile("r")
        writer = sock.makefile("w")

        for message in ["hello", "from the", "unix socket client", "QUIT"]:
            writer.write(message + "\n")
            writer.flush()
            if message == "QUIT":
                break
            echo = reader.readline().rstrip("\n")
            print(f"[client] sent {message!r}, received {echo!r}")


if __name__ == "__main__":
    run_client()
