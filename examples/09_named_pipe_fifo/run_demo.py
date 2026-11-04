"""
Convenience runner: starts reader.py in a separate process (it blocks on
open() until a writer shows up), then runs writer.py in this process, and
cleans up the FIFO file afterwards.

Run:
    python3 run_demo.py
"""
import multiprocessing as mp
import os
import time

from reader import run_reader, FIFO_PATH
from writer import run_writer


def main() -> None:
    reader_process = mp.Process(target=run_reader)
    reader_process.start()
    time.sleep(0.3)  # give the reader a moment to open the FIFO and block

    run_writer()

    reader_process.join(timeout=2)
    if os.path.exists(FIFO_PATH):
        os.unlink(FIFO_PATH)


if __name__ == "__main__":
    main()
