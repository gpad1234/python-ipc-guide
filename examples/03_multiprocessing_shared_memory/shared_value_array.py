"""
multiprocessing.Value / multiprocessing.Array example.

A shared counter (Value) incremented by several worker processes using a
lock, plus a shared fixed-size Array that each worker writes one slot of.

Run:
    python3 shared_value_array.py
"""
import multiprocessing as mp

NUM_WORKERS = 4
INCREMENTS_PER_WORKER = 10_000


def increment_counter(counter: "mp.Value", lock: "mp.Lock") -> None:
    for _ in range(INCREMENTS_PER_WORKER):
        with lock:  # without the lock, concurrent += is NOT atomic
            counter.value += 1


def write_slot(shared_array: "mp.Array", index: int, value: int) -> None:
    shared_array[index] = value


def main() -> None:
    # 'i' = C signed int. See the `array` module docs for all type codes.
    counter = mp.Value("i", 0)
    lock = mp.Lock()

    workers = [
        mp.Process(target=increment_counter, args=(counter, lock))
        for _ in range(NUM_WORKERS)
    ]
    for w in workers:
        w.start()
    for w in workers:
        w.join()

    expected = NUM_WORKERS * INCREMENTS_PER_WORKER
    print(f"[counter] expected={expected} actual={counter.value} "
          f"(match={counter.value == expected})")

    # Shared Array: pre-sized, each worker fills its own slot (no lock
    # needed here since each process writes a distinct index).
    shared_array = mp.Array("i", NUM_WORKERS)
    writers = [
        mp.Process(target=write_slot, args=(shared_array, i, i * i))
        for i in range(NUM_WORKERS)
    ]
    for w in writers:
        w.start()
    for w in writers:
        w.join()

    print(f"[array] contents: {list(shared_array)}")


if __name__ == "__main__":
    main()
