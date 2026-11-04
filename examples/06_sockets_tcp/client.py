"""
TCP socket client: connects to server.py, sends a few lines, prints echoes.

Run standalone (after starting server.py in another terminal):
    python3 client.py
"""
import socket

HOST = "127.0.0.1"
PORT = 50_007


def run_client() -> None:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((HOST, PORT))
        reader = sock.makefile("r")
        writer = sock.makefile("w")

        for message in ["hello", "from the", "tcp client", "QUIT"]:
            writer.write(message + "\n")
            writer.flush()
            if message == "QUIT":
                break
            echo = reader.readline().rstrip("\n")
            print(f"[client] sent {message!r}, received {echo!r}")


if __name__ == "__main__":
    run_client()
