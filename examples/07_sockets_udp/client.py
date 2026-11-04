"""
UDP socket client: sends a few datagrams to server.py. No handshake,
no acknowledgment — each send is independent and unreliable by design.

Run standalone (after starting server.py in another terminal):
    python3 client.py
"""
import socket

HOST = "127.0.0.1"
PORT = 50_008


def run_client() -> None:
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        for message in ["hello", "from the", "udp client", "QUIT"]:
            sock.sendto(message.encode(), (HOST, PORT))
            print(f"[client] sent {message!r} (no delivery guarantee)")


if __name__ == "__main__":
    run_client()
