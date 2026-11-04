# 10 — Anonymous Pipes (`os.pipe`, `os.fork`)

## What it is

The lowest-level pipe primitive: `os.pipe()` returns a pair of file
descriptors `(read_fd, write_fd)` connected by an in-kernel buffer. On its
own, this is only useful between related processes, because file
descriptors are normally only inherited by child processes created via
`fork()` (or passed explicitly) — there's no name/path to open it by, unlike
a FIFO (example 09). This is the raw primitive that `multiprocessing.Pipe`
(example 02) and `subprocess` (example 11) build on top of.

## When to use it

- You're building low-level process-spawning infrastructure yourself (most
  application code should prefer `multiprocessing.Pipe` or `subprocess`,
  which wrap this safely).
- Educational value: understanding what's actually happening under the
  pipes you use via higher-level APIs.

## Tradeoffs

- `os.fork()` is POSIX-only and has sharp edges (e.g., interactions with
  threads, buffered I/O, C extensions) — `multiprocessing` and `subprocess`
  exist specifically to hide these pitfalls.
- You must manually close the ends you don't use in each process (e.g., the
  child closes the write end if it's only reading) or you can get stuck
  waiting for EOF that never comes.
- Only connects a parent and its direct children (via fd inheritance) —
  not arbitrary unrelated processes.

## Run it

```bash
python3 example.py
```

Forks a child that writes to the pipe; the parent reads from it.
