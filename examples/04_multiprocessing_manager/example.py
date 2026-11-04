"""
multiprocessing.Manager example: shared dict + shared list across workers.

Run:
    python3 example.py
"""
import multiprocessing as mp


def worker(worker_id: int, shared_dict, shared_list, lock) -> None:
    # Proxy objects support the usual dict/list operations transparently.
    shared_dict[f"worker-{worker_id}"] = worker_id * 100

    with lock:  # list.append isn't atomic across processes; guard it
        shared_list.append(f"worker-{worker_id} says hi")


def main() -> None:
    with mp.Manager() as manager:
        shared_dict = manager.dict()
        shared_list = manager.list()
        lock = manager.Lock()

        workers = [
            mp.Process(target=worker, args=(i, shared_dict, shared_list, lock))
            for i in range(5)
        ]
        for w in workers:
            w.start()
        for w in workers:
            w.join()

        print("[dict]", dict(shared_dict))
        print("[list]", list(shared_list))


if __name__ == "__main__":
    main()
