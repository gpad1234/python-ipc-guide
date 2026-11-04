"""
multiprocessing.Queue example: multiple producers, multiple consumers.

Run:
    python3 example.py
"""
import multiprocessing as mp
import time
import random

NUM_PRODUCERS = 2
NUM_CONSUMERS = 2
ITEMS_PER_PRODUCER = 5
# Sentinel put on the queue once per consumer to tell it to stop.
STOP = "__STOP__"


def producer(producer_id: int, q: "mp.Queue") -> None:
    for i in range(ITEMS_PER_PRODUCER):
        item = f"producer-{producer_id}-item-{i}"
        time.sleep(random.uniform(0.01, 0.05))  # simulate work
        q.put(item)
        print(f"[producer {producer_id}] put {item!r}")


def consumer(consumer_id: int, q: "mp.Queue", results: "mp.Queue") -> None:
    while True:
        item = q.get()  # blocks until an item is available
        if item == STOP:
            break
        time.sleep(random.uniform(0.01, 0.05))  # simulate processing
        results.put(f"consumer-{consumer_id} handled {item}")


def main() -> None:
    work_queue: mp.Queue = mp.Queue()
    results_queue: mp.Queue = mp.Queue()

    producers = [
        mp.Process(target=producer, args=(pid, work_queue))
        for pid in range(NUM_PRODUCERS)
    ]
    consumers = [
        mp.Process(target=consumer, args=(cid, work_queue, results_queue))
        for cid in range(NUM_CONSUMERS)
    ]

    for p in producers + consumers:
        p.start()

    for p in producers:
        p.join()

    # Now that all producers are done, tell each consumer to stop.
    for _ in consumers:
        work_queue.put(STOP)

    for c in consumers:
        c.join()

    results_queue.put(STOP)
    print("\n--- Results ---")
    while True:
        result = results_queue.get()
        if result == STOP:
            break
        print(result)


if __name__ == "__main__":
    main()
