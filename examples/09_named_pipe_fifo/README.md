# 09 — Named Pipes / FIFOs (`os.mkfifo`)

## What it is

A FIFO ("named pipe") is a special file created with `os.mkfifo()`. Unlike
a regular file, it has no stored content — it's a conduit. One process opens
it for writing, another (possibly completely unrelated, with no
parent/child relationship) opens it for reading, and bytes written by the
writer stream through to the reader in order, just like an anonymous pipe,
but addressable by a filesystem path instead of an inherited file
descriptor.

## When to use it

- Two unrelated processes (not started by one spawning the other) need a
  simple byte-stream channel, and you'd rather use a filesystem path than
  set up a socket.
- You want pipe semantics (ordered byte stream, no message framing) but need
  to reference the channel by name from independent scripts/shells (FIFOs
  are also usable directly from the shell, e.g. `mkfifo` + `cat`).

## Tradeoffs

- POSIX-only (not available on native Windows).
- Opening a FIFO for reading **blocks** until a writer opens it (and vice
  versa) — this synchronization is convenient but can deadlock a
  single-process program that tries to open both ends itself without a
  separate thread/process.
- Still just a byte stream: no built-in message boundaries, no built-in
  multiplexing of several writers' output (interleaving is possible).
- The FIFO is a filesystem entry that must be created once and ideally
  removed when done.

## Run it

```bash
python3 run_demo.py
```

Or manually in two terminals (reader first, since it blocks waiting for a
writer):

```bash
# terminal 1
python3 reader.py
# terminal 2
python3 writer.py
```
