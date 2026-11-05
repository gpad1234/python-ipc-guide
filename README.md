# Python Interprocess Communication (IPC) — Learning & Research

A hands-on collection of runnable examples demonstrating the interprocess
communication (IPC) mechanisms available in the Python **standard library**.
Each example is self-contained, documented, and designed to be run directly
so you can observe the mechanism in action.

## Why IPC?

Separate OS processes (unlike threads) do not share memory by default. When
you split work across multiple processes — to get true parallelism past the
GIL, to isolate failures, or to talk to external programs — you need an
explicit channel to exchange data. That channel is IPC.

## What's covered

| # | Mechanism | Module(s) | Same machine only? | Typical use case |
|---|-----------|-----------|---------------------|-------------------|
| 01 | [Multiprocessing Queue](examples/01_multiprocessing_queue) | `multiprocessing.Queue` | Yes | Many-to-many task/result queues between worker processes |
| 02 | [Multiprocessing Pipe](examples/02_multiprocessing_pipe) | `multiprocessing.Pipe` | Yes | Fast 1:1 duplex channel between two processes |
| 03 | [Shared Memory](examples/03_multiprocessing_shared_memory) | `multiprocessing.shared_memory`, `Value`, `Array` | Yes | Zero-copy sharing of large buffers/arrays, counters |
| 04 | [Manager (proxies)](examples/04_multiprocessing_manager) | `multiprocessing.Manager` | Yes | Shared dict/list/lock across many processes, simplest API |
| 05 | [mmap shared file](examples/05_mmap_shared_file) | `mmap` | Yes | Share data via a memory-mapped file, independent of `multiprocessing` |
| 06 | [TCP sockets](examples/06_sockets_tcp) | `socket` | No (network capable) | Client/server communication, can cross machines |
| 07 | [UDP sockets](examples/07_sockets_udp) | `socket` | No (network capable) | Fire-and-forget datagrams, low overhead, no ordering guarantee |
| 08 | [Unix domain sockets](examples/08_unix_domain_socket) | `socket` (`AF_UNIX`) | Yes | Fast local-only socket IPC, used by Docker/daemons |
| 09 | [Named pipes (FIFO)](examples/09_named_pipe_fifo) | `os.mkfifo` | Yes | Unrelated processes exchanging a byte stream via the filesystem |
| 10 | [Anonymous pipes](examples/10_anonymous_pipe_os) | `os.pipe`, `os.fork` | Yes | Low-level parent/child byte stream (building block for higher-level tools) |
| 11 | [Subprocess stdio](examples/11_subprocess_stdio) | `subprocess` | Yes | Talking to a child program via stdin/stdout/stderr |
| 12 | [Signals](examples/12_signals) | `signal`, `os.kill` | Yes | Lightweight notifications/control (no data payload) between processes |

> Note on the `queue` module: `queue.Queue` is **thread-safe, not
> process-safe** — it only works between threads in the same process. The
> process-safe equivalent is `multiprocessing.Queue` (example 01), which is
> why it's listed there instead of a separate "queue" example.

## Learning path

If you're new to IPC, a sensible order is:

1. **01 → 04** (`multiprocessing.*`) — easiest to use, Python-only, great for
   fan-out/fan-in worker pools.
2. **05** (`mmap`) and the shared-memory part of **03** — understand how data
   can be shared without copying/serializing.
3. **10 → 09** (anonymous pipe → named pipe/FIFO) — see the raw OS primitive
   that `multiprocessing.Pipe` and `subprocess` are built on.
4. **11** (`subprocess`) — the most common real-world case: talking to an
   external program.
5. **06 → 08** (sockets) — the general-purpose, network-capable mechanism;
   everything else is effectively a specialization of this.
6. **12** (`signals`) — out-of-band control signals, useful alongside any of
   the above.

## Choosing a mechanism

- **Need to share Python objects between processes you control?**
  → `multiprocessing` (Queue, Pipe, Manager, shared_memory).
- **Need to share large binary/numeric buffers with zero copying?**
  → `multiprocessing.shared_memory` or `mmap`.
- **Need to talk to a process that isn't Python, or might be on another
  machine?** → sockets (TCP/UDP), or `subprocess` if you're the one
  launching it.
- **Processes only on the same machine, want socket-like semantics but
  faster and filesystem-scoped?** → Unix domain sockets or named pipes.
- **Just need to notify a process of an event, no data?** → signals.

## Run the examples from a GUI

A small local web app lets you pick an example, click **Run**, and see its
stdout/stderr, exit code and duration (or **Run all**). Standard library only:

```bash
python3 gui/app.py            # opens http://127.0.0.1:8765
python3 gui/app.py --port 9000 --no-browser
```

It binds to localhost only, runs only the scripts registered in
[gui/app.py](gui/app.py), runs one example at a time (the demos share fixed
ports and `/tmp` paths), and times each run out after 30 seconds.

## Running the examples from the command line

Each `examples/NN_name/` directory contains its own `README.md` with
specifics, plus one or more `.py` files. Examples are self-contained and use
only the standard library — no `pip install` required. Run them directly,
e.g.:

```bash
python3 examples/01_multiprocessing_queue/example.py
```

For two-script examples (sockets, pipes, subprocess), the README in that
folder tells you which script to start first (usually a server/reader) and
which to run second (client/writer). Some examples spawn both sides
automatically from a single script for convenience.

## Platform notes

- Examples use `multiprocessing`'s default start method for the OS you're
  on. On macOS/Linux this is typically `fork` or `spawn`; on Windows it's
  always `spawn`, which requires the `if __name__ == "__main__":` guard —
  all examples already include it.
- **Unix domain sockets** (08), **named pipes/FIFO** (09), and **signals**
  (12) rely on POSIX features and will not work on native Windows (they do
  work under WSL).
- `os.fork()` (used in example 10) is POSIX-only.

## Requirements

- Python 3.8+ (for `multiprocessing.shared_memory`).
- No third-party packages.
