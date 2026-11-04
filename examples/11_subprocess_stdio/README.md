# 11 — `subprocess` (stdin/stdout/stderr)

## What it is

The standard way to launch and communicate with an external program (which
may not even be Python). Python connects the child's stdin/stdout/stderr to
pipes (built on the same OS pipe primitive as example 10), and you read/
write through the `Popen` object (or let `.communicate()` handle it for
you).

## When to use it

- You need to run another program — a CLI tool, a shell script, a different
  language's interpreter — and feed it input and/or capture its output.
- This is the most common IPC need in real applications: wrapping existing
  tools instead of reimplementing their logic.

## Tradeoffs

- `Popen.communicate()` is simplest but buffers everything in memory and
  closes stdin after sending — fine for short-lived, bounded exchanges, not
  for a long-lived interactive back-and-forth.
- Manual streaming (reading/writing `proc.stdin`/`proc.stdout` yourself) is
  more flexible but you must be careful about deadlocks: if both sides'
  pipe buffers fill up because neither is reading, everything hangs (this
  is why `communicate()` uses threads internally).
- You generally need to agree on a message format over stdout, since it's
  just a byte/text stream (no framing) — similar to the pipe/socket
  examples.

## Run it

```bash
python3 parent.py
```

`parent.py` launches `child.py` as a subprocess and demonstrates two styles:
a one-shot `communicate()` call, and a streaming line-by-line exchange.
