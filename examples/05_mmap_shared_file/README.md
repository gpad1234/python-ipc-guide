# 05 — `mmap` (memory-mapped file)

## What it is

`mmap` maps a file (or an anonymous region on POSIX) directly into a
process's address space. Multiple independent processes can `mmap()` the
*same* file and see each other's writes immediately, without going through
read()/write() system calls each time, and without using `multiprocessing`
at all. This is the lower-level primitive several higher-level tools
(including database engines and `multiprocessing.shared_memory` on some
platforms) are built on.

## When to use it

- You want shared memory between processes that aren't necessarily started
  via `multiprocessing` (e.g., a separate program written in another
  language, or processes started independently).
- You want the shared region to be backed by a real file (so it can persist,
  or be inspected with normal file tools).
- You need fine control over the shared layout (fixed offsets/fields),
  similar to a struct.

## Tradeoffs

- No built-in synchronization — you must coordinate access yourself (locks,
  semaphores, or your own protocol), just like with `shared_memory`.
- Being backed by a real file means the OS may write dirty pages to disk;
  for pure in-memory sharing, `multiprocessing.shared_memory` (example 03)
  is simpler on POSIX/Windows alike.
- Fixed-size region: resizing is possible but clunky (`mmap.resize`, not
  supported on all platforms).

## Run it

```bash
python3 example.py
```

The script creates a backing file, maps it, spawns a child process that
maps the same file and mutates it, and the parent observes the change.
