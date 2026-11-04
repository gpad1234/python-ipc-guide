"""
UDP socket server: receives datagrams and prints them. Stops after
receiving a "QUIT" datagram.

Run standalone:
    python3 server.py
Then in another terminal:
    python3 client.py
"""
import socket

HOST = "127.0.0.1"
PORT = 50_008


def run_server(ready=None) -> None:
    """
    `ready`, if given, is an mp.Event that gets set right after bind() so a
    caller can wait for it before sending — UDP has no handshake, so any
    datagram sent before the socket is bound is simply lost.
    """
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.bind((HOST, PORT))
        print(f"[server] listening for datagrams on {HOST}:{PORT}")
        if ready is not None:
            ready.set()
        sock.settimeout(10)  # safety net: never block forever in this demo
        while True:
            try:
                data, addr = sock.recvfrom(1024)
            except socket.timeout:
                print("[server] timed out waiting for datagrams, stopping")
                break
            message = data.decode()
            print(f"[server] received {message!r} from {addr}")
            if message == "QUIT":
                break
    print("[server] stopped")


if __name__ == "__main__":
    run_server()
