# 01 — `multiprocessing.Queue`

## What it is

A FIFO queue that is safe to use from multiple processes at once. Internally
it pickles objects, sends their bytes through an `os.pipe()` (example 10),
and unpickles them on the receiving end. Unlike `queue.Queue` (threading),
this one actually copies data across the process boundary.

## When to use it

- Many-to-many communication: several producer processes feeding several
  consumer/worker processes.
- Distributing tasks to a worker pool and collecting results.
- You don't need the absolute lowest latency, just a simple, safe channel.

## Tradeoffs

- Every item is pickled/unpickled — there's serialization overhead, so it's
  not ideal for huge payloads at high frequency (see `shared_memory`,
  example 03, for that).
- Queue size/order guarantees are best-effort across processes; `qsize()` is
  unreliable on some platforms (notably macOS).
- A `multiprocessing.Queue` must not be shared via `Manager` *and* put/get
  used from `ThreadPoolExecutor` threads indiscriminately without care — it
  works, but keep ownership simple.

## Run it

```bash
python3 example.py
```

The script starts two producer processes and two consumer processes sharing
one queue, then prints the results as they're consumed.
