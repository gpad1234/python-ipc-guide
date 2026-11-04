"""
Raw os.pipe() + os.fork() example (POSIX only).

The child writes a few messages into the pipe and exits; the parent reads
them until it sees EOF (i.e., all writers have closed the write end).

Run:
    python3 example.py
"""
import os
import sys


def main() -> None:
    read_fd, write_fd = os.pipe()

    pid = os.fork()

    if pid == 0:
        # --- Child process ---
        os.close(read_fd)  # the child only writes, so close its read end
        with os.fdopen(write_fd, "w") as writer:
            for message in ["hello from child", "second message", "bye"]:
                writer.write(message + "\n")
                writer.flush()
        # write end closes automatically when the `with` block exits;
        # that's what lets the parent's read() see EOF.
        os._exit(0)  # os._exit skips Python cleanup that would duplicate
                      # the parent's atexit handlers after a fork
    else:
        # --- Parent process ---
        os.close(write_fd)  # the parent only reads, so close its write end
        with os.fdopen(read_fd, "r") as reader:
            for line in reader:
                print(f"[parent] received: {line.rstrip()!r}")
        os.waitpid(pid, 0)  # reap the child to avoid a zombie process
        print("[parent] child has exited, pipe closed (EOF)")


if __name__ == "__main__":
    if not hasattr(os, "fork"):
        print("os.fork() is not available on this platform (Windows).",
              file=sys.stderr)
        sys.exit(1)
    main()
