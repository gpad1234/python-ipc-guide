# 06 — TCP Sockets (`socket`, `AF_INET`/`SOCK_STREAM`)

## What it is

The general-purpose, network-capable IPC mechanism. A TCP socket provides a
reliable, ordered, byte-stream connection between two endpoints identified
by `(host, port)`. The two endpoints can be on the same machine or across a
network — the API is identical either way.

## When to use it

- Processes may run on **different machines**, or you want that option
  later without rewriting the IPC layer.
- You need a reliable, ordered stream (TCP handles retransmission/ordering
  for you).
- You're talking to a process not written in Python (TCP is language/OS
  agnostic).

## Tradeoffs

- More ceremony than `multiprocessing` primitives: you manage connection
  setup/teardown, framing (TCP has no message boundaries — you must define
  your own, e.g. length-prefixing or newline-delimited messages), and
  errors.
- Overhead of the TCP/IP stack, even on localhost, is higher than a Unix
  domain socket or pipe.
- No built-in serialization — you decide the wire format (this example uses
  simple newline-delimited UTF-8 text).

## Run it

This example spawns the server and client as separate processes from one
script for convenience:

```bash
python3 run_demo.py
```

Or run them in two terminals to see it more realistically:

```bash
# terminal 1
python3 server.py
# terminal 2
python3 client.py
```
