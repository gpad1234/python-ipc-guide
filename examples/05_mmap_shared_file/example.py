"""
mmap example: two independent processes share a memory-mapped file.

Run:
    python3 example.py
"""
import mmap
import multiprocessing as mp
import os
import tempfile

SIZE = 64


def child_task(path: str, ready: "mp.Event", done: "mp.Event") -> None:
    fd = os.open(path, os.O_RDWR)
    try:
        mm = mmap.mmap(fd, SIZE)
        ready.wait()  # wait for the parent to write first
        print(f"[child] read: {mm[0:11]!r}")
        mm[0:11] = b"goodbye!!!!"
        mm.flush()
        mm.close()
    finally:
        os.close(fd)
    done.set()


def main() -> None:
    # A real backing file on disk; both processes open it independently.
    tmp = tempfile.NamedTemporaryFile(prefix="ipc-mmap-", delete=False)
    path = tmp.name
    tmp.write(b"\x00" * SIZE)
    tmp.flush()
    tmp.close()

    try:
        fd = os.open(path, os.O_RDWR)
        mm = mmap.mmap(fd, SIZE)
        mm[0:11] = b"hello there"

        ready = mp.Event()
        done = mp.Event()
        p = mp.Process(target=child_task, args=(path, ready, done))
        p.start()
        ready.set()
        done.wait()
        p.join()

        # The parent sees the child's write because both map the same file.
        print(f"[parent] bytes after child wrote: {mm[0:11]!r}")

        mm.close()
        os.close(fd)
    finally:
        os.unlink(path)  # clean up the backing file


if __name__ == "__main__":
    main()
