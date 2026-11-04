"""
Convenience runner: starts server.py and client.py as separate processes so
you can see the full exchange with a single command.

Run:
    python3 run_demo.py
"""
import multiprocessing as mp

from server import run_server
from client import run_client


def main() -> None:
    ready = mp.Event()
    server_process = mp.Process(target=run_server, args=(ready,))
    server_process.start()
    # Wait for the server to actually bind before sending — UDP has no
    # handshake, so datagrams sent before bind() would just be lost.
    ready.wait(timeout=5)

    run_client()

    server_process.join(timeout=12)


if __name__ == "__main__":
    main()
