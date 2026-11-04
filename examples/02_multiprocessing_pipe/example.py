"""
multiprocessing.Pipe example: duplex request/response between a parent
and a single child process.

Run:
    python3 example.py
"""
import multiprocessing as mp


def child(conn: "mp.connection.Connection") -> None:
    """Receives requests, sends back a response, until told to stop."""
    while True:
        request = conn.recv()
        if request == "STOP":
            conn.close()
            break
        response = f"squared({request}) = {request ** 2}"
        conn.send(response)


def main() -> None:
    parent_conn, child_conn = mp.Pipe()  # duplex=True by default

    p = mp.Process(target=child, args=(child_conn,))
    p.start()

    for n in range(5):
        parent_conn.send(n)
        response = parent_conn.recv()
        print(f"[parent] sent {n}, got back: {response}")

    parent_conn.send("STOP")
    p.join()
    print("[parent] child process finished")


if __name__ == "__main__":
    main()
