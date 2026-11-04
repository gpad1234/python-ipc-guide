"""
Parent program demonstrating two ways to use subprocess for IPC with
child.py:

1. One-shot: Popen.communicate() — send all input at once, get all
   output back at once, then the process exits. Simple, but not suitable
   for a long interactive session.
2. Streaming: write/read line-by-line while the child process stays alive,
   using unbuffered pipes.

Run:
    python3 parent.py
"""
import os
import subprocess
import sys

CHILD_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "child.py")
CHILD = [sys.executable, CHILD_PATH]


def one_shot_demo() -> None:
    print("--- one-shot communicate() demo ---")
    input_text = "hello\nworld\nQUIT\n"
    result = subprocess.run(
        CHILD,
        input=input_text,
        capture_output=True,
        text=True,
        check=True,
    )
    print(f"[parent] child stdout:\n{result.stdout.rstrip()}")


def streaming_demo() -> None:
    print("\n--- streaming demo ---")
    proc = subprocess.Popen(
        CHILD,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        text=True,
        bufsize=1,  # line-buffered, so each write/read happens promptly
    )
    try:
        for message in ["foo", "bar", "baz"]:
            proc.stdin.write(message + "\n")
            proc.stdin.flush()
            response = proc.stdout.readline().rstrip("\n")
            print(f"[parent] sent {message!r}, got back {response!r}")

        proc.stdin.write("QUIT\n")
        proc.stdin.flush()
    finally:
        proc.stdin.close()
        proc.wait(timeout=5)
    print(f"[parent] child exited with code {proc.returncode}")


def main() -> None:
    one_shot_demo()
    streaming_demo()


if __name__ == "__main__":
    main()
