"""
Local web GUI for running the IPC examples and viewing their output.

Run:
    python3 gui/app.py            # then open http://127.0.0.1:8765
    python3 gui/app.py --port 9000

Standard library only. Binds to localhost and only runs the scripts listed
in the registry below (the browser never supplies a path or command).
"""
import argparse
import json
import subprocess
import sys
import threading
import time
import webbrowser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EXAMPLES_DIR = ROOT / "examples"
INDEX_HTML = Path(__file__).resolve().parent / "index.html"
RUN_TIMEOUT = 30

# (id, title, folder, script)
_REGISTRY = [
    ("queue", "multiprocessing.Queue", "01_multiprocessing_queue", "example.py"),
    ("pipe", "multiprocessing.Pipe", "02_multiprocessing_pipe", "example.py"),
    ("shm-value", "Shared Value / Array", "03_multiprocessing_shared_memory", "shared_value_array.py"),
    ("shm-block", "SharedMemory block", "03_multiprocessing_shared_memory", "shared_block.py"),
    ("manager", "multiprocessing.Manager", "04_multiprocessing_manager", "example.py"),
    ("mmap", "mmap shared file", "05_mmap_shared_file", "example.py"),
    ("tcp", "TCP sockets", "06_sockets_tcp", "run_demo.py"),
    ("udp", "UDP sockets", "07_sockets_udp", "run_demo.py"),
    ("unix", "Unix domain sockets", "08_unix_domain_socket", "run_demo.py"),
    ("fifo", "Named pipe (FIFO)", "09_named_pipe_fifo", "run_demo.py"),
    ("os-pipe", "Anonymous pipe (os.pipe)", "10_anonymous_pipe_os", "example.py"),
    ("subprocess", "subprocess stdio", "11_subprocess_stdio", "parent.py"),
    ("signals", "Signals", "12_signals", "example.py"),
]
EXAMPLES = {
    ex_id: {"id": ex_id, "title": title, "folder": folder, "script": script}
    for ex_id, title, folder, script in _REGISTRY
}

# The demos share fixed ports and /tmp paths, so only one may run at a time.
_run_lock = threading.Lock()


def _readme_summary(folder: str) -> str:
    """First paragraph under '## What it is' in the example's README."""
    readme = EXAMPLES_DIR / folder / "README.md"
    try:
        lines = readme.read_text(encoding="utf-8").splitlines()
    except OSError:
        return ""
    para, started = [], False
    for line in lines:
        if line.startswith("## What it is"):
            started = True
        elif started:
            if line.startswith("#"):
                break
            if line.strip():
                para.append(line.strip())
            elif para:
                break
    return " ".join(para)


def list_examples() -> list:
    out = []
    for ex in _REGISTRY:
        info = dict(EXAMPLES[ex[0]])
        info["summary"] = _readme_summary(info["folder"])
        out.append(info)
    return out


def _txt(value) -> str:
    if isinstance(value, bytes):
        return value.decode(errors="replace")
    return value or ""


def run_example(ex_id: str) -> dict:
    ex = EXAMPLES.get(ex_id)
    if ex is None:
        return {"error": f"unknown example {ex_id!r}"}
    if not _run_lock.acquire(blocking=False):
        return {"error": "another example is already running; try again shortly"}
    try:
        cwd = EXAMPLES_DIR / ex["folder"]
        start = time.monotonic()
        try:
            proc = subprocess.run(
                [sys.executable, "-u", ex["script"]],
                cwd=cwd,
                capture_output=True,
                text=True,
                timeout=RUN_TIMEOUT,
            )
            result = {
                "stdout": proc.stdout,
                "stderr": proc.stderr,
                "exit_code": proc.returncode,
                "timed_out": False,
            }
        except subprocess.TimeoutExpired as e:
            result = {
                "stdout": _txt(e.stdout),
                "stderr": _txt(e.stderr),
                "exit_code": None,
                "timed_out": True,
            }
        result["duration"] = round(time.monotonic() - start, 2)
        result["id"] = ex_id
        return result
    finally:
        _run_lock.release()


class Handler(BaseHTTPRequestHandler):
    def _send(self, status: int, body: bytes, ctype: str) -> None:
        self.send_response(status)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def _json(self, obj, status: int = 200) -> None:
        self._send(status, json.dumps(obj).encode(), "application/json")

    def _local_origin_ok(self) -> bool:
        # Reject other websites (CSRF) and DNS-rebinding hosts.
        host = self.headers.get("Host", "")
        origin = self.headers.get("Origin")
        if host.rsplit(":", 1)[0] not in ("127.0.0.1", "localhost"):
            return False
        return origin is None or origin.split("://", 1)[-1] == host

    def do_GET(self) -> None:
        if not self._local_origin_ok():
            return self._json({"error": "forbidden"}, 403)
        if self.path in ("/", "/index.html"):
            self._send(200, INDEX_HTML.read_bytes(), "text/html; charset=utf-8")
        elif self.path == "/api/examples":
            self._json(list_examples())
        else:
            self._json({"error": "not found"}, 404)

    def do_POST(self) -> None:
        if not self._local_origin_ok():
            return self._json({"error": "forbidden"}, 403)
        if self.path != "/api/run":
            return self._json({"error": "not found"}, 404)
        try:
            length = int(self.headers.get("Content-Length", 0))
            payload = json.loads(self.rfile.read(length) or b"{}")
            ex_id = payload.get("id")
        except (ValueError, AttributeError):
            return self._json({"error": "bad request"}, 400)
        result = run_example(ex_id)
        self._json(result, 400 if "error" in result else 200)

    def log_message(self, fmt, *args) -> None:
        sys.stderr.write("[gui] " + fmt % args + "\n")


def main() -> None:
    parser = argparse.ArgumentParser(description="IPC example runner GUI")
    parser.add_argument("--port", type=int, default=8765)
    parser.add_argument("--no-browser", action="store_true")
    args = parser.parse_args()

    server = ThreadingHTTPServer(("127.0.0.1", args.port), Handler)
    url = f"http://127.0.0.1:{args.port}"
    print(f"IPC example runner at {url}  (Ctrl+C to stop)")
    if not args.no_browser:
        webbrowser.open(url)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
