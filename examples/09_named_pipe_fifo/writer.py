"""
FIFO writer: opens the named pipe for writing and sends a few lines.

Run standalone (after starting reader.py in another terminal, since opening
the FIFO for writing blocks until a reader is present):
    python3 writer.py
"""
import os

FIFO_PATH = "/tmp/ipc-demo.fifo"


def run_writer() -> None:
    if not os.path.exists(FIFO_PATH):
        os.mkfifo(FIFO_PATH)

    with open(FIFO_PATH, "w") as fifo:
        for message in ["hello", "from the", "fifo writer", "QUIT"]:
            fifo.write(message + "\n")
            fifo.flush()
            print(f"[writer] sent: {message!r}")


if __name__ == "__main__":
    run_writer()
