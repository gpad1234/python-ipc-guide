"""
Child program for the subprocess example. Reads lines from stdin, and for
each one prints an uppercased, reversed version to stdout, flushing
immediately so the parent can read it right away in streaming mode. Stops
on EOF or a "QUIT" line.
"""
import sys


def main() -> None:
    for line in sys.stdin:
        line = line.rstrip("\n")
        if line == "QUIT":
            break
        print(line.upper()[::-1], flush=True)


if __name__ == "__main__":
    main()
