"""
Convenience runner: starts server.py and client.py as separate processes so
you can see the full exchange with a single command.

Run:
    python3 run_demo.py
"""
import multiprocessing as mp
import time

from server import run_server
from client import run_client


def main() -> None:
    server_process = mp.Process(target=run_server)
    server_process.start()
    time.sleep(0.3)  # give the server a moment to bind and start listening

    run_client()

    server_process.join(timeout=2)


if __name__ == "__main__":
    main()
