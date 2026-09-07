from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import json
import os
import platform
import socket
import time

import psutil

BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"

BOOT_TIME = psutil.boot_time()
LAST_NET = psutil.net_io_counters()
LAST_NET_TIME = time.time()


def bytes_to_gb(value):
    return round(value / (1024 ** 3), 2)


def get_local_ip():
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.connect(("8.8.8.8", 80))
        ip = sock.getsockname()[0]
        sock.close()
        return ip
    except OSError:
        return "Unavailable"


def get_stats():
    global LAST_NET, LAST_NET_TIME

    cpu = psutil.cpu_percent(interval=0.15)
    memory = psutil.virtual_memory()
    disk = psutil.disk_usage(os.path.abspath(os.sep))
    current_net = psutil.net_io_counters()
    now = time.time()

    elapsed = max(now - LAST_NET_TIME, 0.001)
    down_rate = (current_net.bytes_recv - LAST_NET.bytes_recv) / elapsed
    up_rate = (current_net.bytes_sent - LAST_NET.bytes_sent) / elapsed

    LAST_NET = current_net
    LAST_NET_TIME = now

    uptime_seconds = int(time.time() - BOOT_TIME)
    hours, remainder = divmod(uptime_seconds, 3600)
    minutes, _ = divmod(remainder, 60)

    return {
        "hostname": socket.gethostname(),
        "os": f"{platform.system()} {platform.release()}",
        "processor": platform.processor() or "Unknown CPU",
        "local_ip": get_local_ip(),
        "cpu_percent": round(cpu, 1),
        "ram_percent": round(memory.percent, 1),
        "ram_used_gb": bytes_to_gb(memory.used),
        "ram_total_gb": bytes_to_gb(memory.total),
        "disk_percent": round(disk.percent, 1),
        "disk_used_gb": bytes_to_gb(disk.used),
        "disk_total_gb": bytes_to_gb(disk.total),
        "download_kbps": round(down_rate / 1024, 1),
        "upload_kbps": round(up_rate / 1024, 1),
        "process_count": len(psutil.pids()),
        "uptime": f"{hours}h {minutes}m",
        "status": "HEALTHY" if cpu < 90 and memory.percent < 90 and disk.percent < 95 else "CHECK SYSTEM",
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
    }


class DashboardHandler(SimpleHTTPRequestHandler):
    def translate_path(self, path):
        clean = path.split("?", 1)[0].split("#", 1)[0]

        if clean in ("", "/"):
            return str(STATIC_DIR / "index.html")

        requested = clean.lstrip("/")
        return str(STATIC_DIR / requested)

    def do_GET(self):
        if self.path.startswith("/api/stats"):
            payload = json.dumps(get_stats()).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Cache-Control", "no-store")
            self.send_header("Content-Length", str(len(payload)))
            self.end_headers()
            self.wfile.write(payload)
            return

        super().do_GET()

    def log_message(self, format, *args):
        if not self.path.startswith("/api/stats"):
            super().log_message(format, *args)


if __name__ == "__main__":
    host = "127.0.0.1"
    port = 8080
    print(f"\nASH SYSTEM MONITOR")
    print(f"Open http://{host}:{port} in your browser")
    print("Press Ctrl+C to stop.\n")

    server = ThreadingHTTPServer((host, port), DashboardHandler)

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down...")
    finally:
        server.server_close()
