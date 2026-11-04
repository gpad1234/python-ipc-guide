# 03 — Shared Memory (`multiprocessing.shared_memory`, `Value`, `Array`)

## What it is

True shared memory: a block of RAM that multiple processes map into their
own address space and read/write **without pickling or copying** on every
access. The standard library offers a few flavors:

- `multiprocessing.shared_memory.SharedMemory` — a raw named block of bytes,
  great for pairing with `numpy` arrays or custom structures (no numpy used
  here, kept stdlib-only, see `shared_block.py`).
- `multiprocessing.Value` / `multiprocessing.Array` — simple typed shared
  scalars/arrays with an optional built-in lock, ideal for counters and
  small fixed-size data (see `shared_value_array.py`).

## When to use it

- You need to share a large buffer (e.g., image data, numeric arrays)
  between processes and copying it through a `Queue`/`Pipe` would be too
  slow.
- You need a simple shared counter or flag that many worker processes
  increment/read (`Value`).
- You're willing to manage synchronization yourself (locks) since shared
  memory gives you no ordering guarantees for free.

## Tradeoffs

- No automatic synchronization for `SharedMemory` — you must coordinate
  access yourself (e.g., with a `multiprocessing.Lock`).
- `SharedMemory` blocks are OS resources: you must `close()` in every
  process and `unlink()` exactly once (usually from the creator) or you'll
  leak memory segments that outlive your Python process.
- `Value`/`Array` require you to declare a fixed C-compatible type (`'i'`,
  `'d'`, etc.) up front — not for arbitrary Python objects (use `Manager`,
  example 04, for that).

## Run it

```bash
python3 shared_value_array.py
python3 shared_block.py
```
