# 08 — Unix Domain Sockets (`socket`, `AF_UNIX`)

## What it is

Like a TCP socket, but addressed by a path on the filesystem instead of a
`(host, port)` pair, and restricted to the local machine. Because the kernel
doesn't need to go through the network stack (no IP routing, checksums,
etc.), it's generally faster than a TCP socket on localhost. This is the
mechanism behind things like the Docker daemon socket (`/var/run/docker.sock`)
and many database client libraries' local connection mode.

## When to use it

- Both endpoints are guaranteed to be on the same machine, and you want
  socket semantics (streams, `SOCK_STREAM` or datagrams, `SOCK_DGRAM`) with
  less overhead than TCP.
- You want filesystem permissions (owner/group/mode on the socket file) to
  control who can connect — a built-in access-control mechanism TCP
  localhost sockets don't have.
- You're building a local daemon/service that other local processes connect
  to.

## Tradeoffs

- POSIX-only (no native Windows support; not available in this form on
  Windows, though newer Windows versions have added limited `AF_UNIX`
  support — not covered here).
- The socket is a filesystem entry: you must `unlink()` (delete) a stale
  socket file before re-binding, and clean it up after use.
- Still requires you to define your own message framing, same as TCP.

## Run it

```bash
python3 run_demo.py
```
