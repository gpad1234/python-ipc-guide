# 07 — UDP Sockets (`socket`, `AF_INET`/`SOCK_DGRAM`)

## What it is

A connectionless, message-oriented protocol. Each `sendto()` is one discrete
datagram; the OS does **not** guarantee delivery, ordering, or that large
datagrams won't be dropped. There's no handshake — the "server" just binds a
port and waits for packets to arrive.

## When to use it

- Low-latency, fire-and-forget data where occasional loss is acceptable
  (metrics/telemetry, live video/audio frames, service discovery).
- Broadcast/multicast scenarios (not shown here, but UDP supports them;
  TCP does not).
- You want to avoid the overhead of connection setup for many small,
  independent messages.

## Tradeoffs

- No reliability: messages can be lost, duplicated, or arrive out of order.
  You must build your own acknowledgment/retry logic if you need it.
- Message size is bounded by the OS/network MTU in practice (even though
  the API allows larger datagrams, they may get silently dropped or
  fragmented).
- No built-in flow control — a fast sender can overwhelm a slow receiver's
  socket buffer.

## Run it

```bash
python3 run_demo.py
```
