"""
multiprocessing.shared_memory.SharedMemory example.

The main process creates a named shared memory block, writes some bytes
into it, and a child process attaches to it by name and reads/modifies it.
Demonstrates manual synchronization with an Event, and proper cleanup
(close in every process, unlink only once).

Run:
    python3 shared_block.py
"""
import multiprocessing as mp
from multiprocessing import shared_memory

BLOCK_SIZE = 32
SHM_NAME = "ipc-demo-block"


def child_task(name: str, ready: "mp.Event", done: "mp.Event") -> None:
    # Attach to the existing block by name (do not create a new one).
    shm = shared_memory.SharedMemory(name=name)
    ready.wait()  # wait until the parent has written its data
    print(f"[child] read bytes: {bytes(shm.buf[:13])!r}")

    # Mutate the buffer in place; the parent will see this change too.
    shm.buf[0:5] = b"HELLO"
    shm.close()  # detach from this process; the block itself still exists
    done.set()


def main() -> None:
    # Clean up any leftover block from a previous crashed run, if present.
    try:
        stale = shared_memory.SharedMemory(name=SHM_NAME)
        stale.close()
        stale.unlink()
    except FileNotFoundError:
        pass

    shm = shared_memory.SharedMemory(name=SHM_NAME, create=True, size=BLOCK_SIZE)
    shm.buf[0:13] = b"hello, child!"

    ready = mp.Event()
    done = mp.Event()
    p = mp.Process(target=child_task, args=(SHM_NAME, ready, done))
    p.start()
    ready.set()  # tell the child the data is ready to read
    done.wait()  # wait for the child to mutate the buffer
    p.join()

    print(f"[parent] bytes after child wrote: {bytes(shm.buf[0:5])!r}")

    # Every process that opened the block must close() it...
    shm.close()
    # ...and exactly one process (the creator, typically) must unlink()
    # it to release the OS resource. Failing to do so leaks shared memory
    # that persists even after your Python process exits.
    shm.unlink()


if __name__ == "__main__":
    main()
