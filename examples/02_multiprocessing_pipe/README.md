# 02 — `multiprocessing.Pipe`

## What it is

A pair of connected `Connection` objects (like a bidirectional socket) backed
by `os.pipe()` under the hood. By default it's **duplex** (both ends can
send and receive); you can request a one-way (simplex) pipe.

## When to use it

- Exactly **two** processes need to talk (parent/child, or two workers you
  spawn together).
- You want lower overhead than `Queue` for a dedicated 1:1 channel.
- You need request/response style communication between exactly two
  endpoints.

## Tradeoffs

- Only connects two endpoints — not suitable for many-to-many (use `Queue`
  or a `Manager` for that).
- If you `send()` large objects faster than the other end `recv()`s them,
  the OS pipe buffer can fill up and block the sender.
- Corruption from concurrent `send()`/`recv()` calls by multiple processes
  on the *same* end is possible — give each end to a single process.

## Run it

```bash
python3 example.py
```

Spawns a single child process; parent and child exchange a few request/
response messages over the pipe.
