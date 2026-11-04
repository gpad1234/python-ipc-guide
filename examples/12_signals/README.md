# 12 — Signals (`signal`, `os.kill`)

## What it is

Unix signals are an asynchronous, lightweight notification mechanism built
into the OS. A process can send a signal (e.g., `SIGUSR1`, `SIGTERM`) to
another process it has permission to signal, and the receiving process can
install a handler that runs when the signal arrives — interrupting whatever
it was doing. Unlike every other mechanism in this repo, signals carry
**no data payload** (beyond which signal number it was) — they're a control
channel, not a data channel.

## When to use it

- You need to notify another process of an event (reload config, shut down
  gracefully, dump stats) without the overhead of a socket/pipe.
- Implementing graceful shutdown (`SIGTERM`) or custom application-defined
  notifications (`SIGUSR1`/`SIGUSR2`, the two signals reserved for
  application use).
- Combining with another IPC mechanism: e.g., "SIGUSR1 means check the
  shared memory block / queue for new data" is a common pattern.

## Tradeoffs

- No payload — if you need to send data, you still need a second channel
  (queue, shared memory, socket) and use the signal purely to say "look
  now."
- Signal handlers run with real restrictions (should do minimal work,
  avoid most I/O/locking — "async-signal-safety"); this example keeps
  handlers simple (just setting a flag) for that reason.
- `SIGUSR1`/`SIGUSR2`/`os.kill` are POSIX concepts; Windows has a very
  limited signal model (mainly `SIGINT`/`SIGBREAK`/`SIGTERM`) and no
  `os.kill` targeting arbitrary signals in the same way.

## Run it

```bash
python3 example.py
```

The parent spawns a child that installs a `SIGUSR1` handler, then the
parent sends it a few signals via `os.kill`, and finally asks it to stop
with `SIGTERM`.
