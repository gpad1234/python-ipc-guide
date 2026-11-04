"""
Signals example: parent sends SIGUSR1 (custom notification) and SIGTERM
(shutdown request) to a child process.

Run:
    python3 example.py

Note: POSIX only (macOS/Linux). Will not work on native Windows.
"""
import multiprocessing as mp
import os
import signal
import sys
import time


def child_task(ready: "mp.Event") -> None:
    received_count = 0

    def handle_sigusr1(signum, frame) -> None:
        nonlocal received_count
        received_count += 1
        # Signal handlers should stay minimal; a simple print is fine for
        # this demo but avoid heavy work/locking in real handlers.
        print(f"[child pid={os.getpid()}] got SIGUSR1 (count={received_count})")

    def handle_sigterm(signum, frame) -> None:
        print(f"[child pid={os.getpid()}] got SIGTERM, shutting down "
              f"(received {received_count} SIGUSR1 total)")
        sys.exit(0)

    signal.signal(signal.SIGUSR1, handle_sigusr1)
    signal.signal(signal.SIGTERM, handle_sigterm)

    ready.set()  # tell the parent our handlers are installed
    while True:
        signal.pause()  # sleep until any signal arrives, then loop


def main() -> None:
    if not hasattr(signal, "SIGUSR1"):
        print("SIGUSR1 is not available on this platform (Windows).",
              file=sys.stderr)
        sys.exit(1)

    ready = mp.Event()
    child = mp.Process(target=child_task, args=(ready,))
    child.start()
    ready.wait()  # don't send signals before the handler is installed

    for _ in range(3):
        time.sleep(0.2)
        os.kill(child.pid, signal.SIGUSR1)
        print(f"[parent] sent SIGUSR1 to pid={child.pid}")

    time.sleep(0.2)
    os.kill(child.pid, signal.SIGTERM)
    print(f"[parent] sent SIGTERM to pid={child.pid}")

    child.join(timeout=2)
    print(f"[parent] child exit code: {child.exitcode}")


if __name__ == "__main__":
    main()
