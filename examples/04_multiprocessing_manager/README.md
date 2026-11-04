# 04 — `multiprocessing.Manager`

## What it is

A `Manager` starts a dedicated server process that holds Python objects
(dict, list, Namespace, Lock, etc.) and hands out *proxy* objects to other
processes. Operations on the proxy are transparently forwarded to the real
object over an internal connection (a pipe/socket) and pickled, so it feels
like you're sharing arbitrary Python objects — at the cost of a network-call
style round trip per operation.

## When to use it

- You want a shared `dict` or `list` across many processes and don't want to
  manage a `Lock` + `shared_memory` block yourself.
- Prototyping / simplicity matters more than raw throughput.
- You need structures `shared_memory`/`Value`/`Array` can't represent
  directly (nested dicts, arbitrary Python objects).

## Tradeoffs

- Much slower than `Value`/`Array`/`shared_memory` — every read/write is a
  method call proxied through the manager process (serialization + IPC each
  time).
- The manager process is a single point of contention; heavy concurrent use
  can bottleneck there.
- If the manager process dies, every proxy becomes unusable.

## Run it

```bash
python3 example.py
```

Several worker processes concurrently update a shared dict and a shared
list managed by one `Manager` process.
