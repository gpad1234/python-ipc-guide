"""
FIFO reader: opens the named pipe for reading and prints each line until
the writer sends "QUIT".

Run standalone (start this first — opening for read blocks until a writer
connects):
    python3 reader.py
Then in another terminal:
    python3 writer.py
"""
import os

FIFO_PATH = "/tmp/ipc-demo.fifo"


def run_reader() -> None:
    if not os.path.exists(FIFO_PATH):
        os.mkfifo(FIFO_PATH)

    print(f"[reader] waiting for a writer to open {FIFO_PATH} ...")
    with open(FIFO_PATH, "r") as fifo:
        print("[reader] writer connected")
        for line in fifo:
            line = line.rstrip("\n")
            if line == "QUIT":
                break
            print(f"[reader] received: {line!r}")
    print("[reader] done")


if __name__ == "__main__":
    run_reader()
