from __future__ import annotations

import asyncio
import time
from collections import deque, defaultdict
from dataclasses import dataclass, asdict
from typing import Any, Dict

import psutil
from quart import request, g


@dataclass
class LatencyStats:
    count: int = 0
    total: float = 0.0
    max: float = 0.0


class RingLatency:
    """Fixed-size ring buffer to approximate quantiles."""

    def __init__(self, size: int = 1024) -> None:
        self._buf: deque[float] = deque(maxlen=size)

    def add(self, value: float) -> None:
        self._buf.append(value)

    def snapshot(self) -> list[float]:
        return list(self._buf)


class Metrics:
    def __init__(self) -> None:
        self._lock = asyncio.Lock()

        # Counters
        self.start_time = time.time()
        self.total_requests = 0
        self.in_flight_requests = 0
        self.total_responses = 0
        self.total_exceptions = 0
        self.status_counts: Dict[int, int] = defaultdict(int)
        self.method_counts: Dict[str, int] = defaultdict(int)
        self.path_counts: Dict[str, int] = defaultdict(int)

        # Streaming/WebSocket
        self.sse_in_flight = 0
        self.ws_connections = 0

        # Latency
        self.latency = LatencyStats()
        self._ring = RingLatency(size=1024)

    async def on_request_start(self) -> None:
        async with self._lock:
            self.total_requests += 1
            self.in_flight_requests += 1
            self.method_counts[request.method] += 1
            # group path to first segment to avoid unbounded cardinality
            path = request.path
            base = "/".join([seg for seg in path.split("/") if seg][:2])
            base = "/" + base if base else "/"
            self.path_counts[base] += 1

    async def on_request_end(self, status_code: int, duration_s: float, is_sse: bool = False) -> None:
        async with self._lock:
            self.in_flight_requests = max(0, self.in_flight_requests - 1)
            self.total_responses += 1
            self.status_counts[int(status_code)] += 1

            # Latency
            self.latency.count += 1
            self.latency.total += duration_s
            if duration_s > self.latency.max:
                self.latency.max = duration_s
            self._ring.add(duration_s)

            if is_sse:
                # SSE streams are short-lived in this app; adjust down if needed
                self.sse_in_flight = max(0, self.sse_in_flight - 1)

    async def on_exception(self) -> None:
        async with self._lock:
            self.total_exceptions += 1

    async def on_sse_start(self) -> None:
        async with self._lock:
            self.sse_in_flight += 1

    async def on_ws_open(self) -> None:
        async with self._lock:
            self.ws_connections += 1

    async def on_ws_close(self) -> None:
        async with self._lock:
            self.ws_connections = max(0, self.ws_connections - 1)

    def _quantiles(self) -> Dict[str, float]:
        arr = sorted(self._ring.snapshot())
        if not arr:
            return {"p50": 0.0, "p90": 0.0, "p95": 0.0, "p99": 0.0}
        def q(p: float) -> float:
            idx = int(p * (len(arr) - 1))
            return arr[idx]
        return {"p50": q(0.50), "p90": q(0.90), "p95": q(0.95), "p99": q(0.99)}

    def to_dict(self) -> Dict[str, Any]:
        uptime = time.time() - self.start_time
        cpu = psutil.cpu_percent(interval=0)
        mem = psutil.Process().memory_info().rss
        threads = psutil.Process().num_threads()
        try:
            open_files = len(psutil.Process().open_files())
        except Exception:
            open_files = None

        avg_latency = (self.latency.total / self.latency.count) if self.latency.count else 0.0
        quant = self._quantiles()

        return {
            "uptime_s": uptime,
            "requests": {
                "total": self.total_requests,
                "in_flight": self.in_flight_requests,
                "responses": self.total_responses,
                "exceptions": self.total_exceptions,
                "by_status": dict(self.status_counts),
                "by_method": dict(self.method_counts),
                "by_path_group": dict(self.path_counts),
            },
            "latency_s": {
                "avg": avg_latency,
                "max": self.latency.max,
                **quant,
            },
            "streams": {
                "sse_in_flight": self.sse_in_flight,
                "ws_connections": self.ws_connections,
            },
            "process": {
                "cpu_percent": cpu,
                "rss_bytes": mem,
                "threads": threads,
                "open_files": open_files,
            },
        }


METRICS = Metrics()


def setup_metrics(app) -> None:
    """Wire metrics into the Quart server and expose a JSON endpoint."""
    server = app.server

    @server.before_request
    async def _before_request():
        # mark start time and bump counters
        g._req_start = time.perf_counter()
        await METRICS.on_request_start()

    @server.after_request
    async def _after_request(response):
        start = getattr(g, "_req_start", None)
        dur = (time.perf_counter() - start) if start is not None else 0.0
        is_sse = False
        try:
            ct = response.headers.get("Content-Type", "")
            if "text/event-stream" in ct:
                is_sse = True
        except Exception:
            pass
        await METRICS.on_request_end(getattr(response, "status_code", 200), dur, is_sse=is_sse)
        return response

    @server.errorhandler(Exception)
    async def _on_error(e):
        await METRICS.on_exception()
        raise e

    @server.get("/__metrics")
    async def _metrics_endpoint():
        data = METRICS.to_dict()
        # augment with request host so CLI can infer server address/port
        try:
            data["server"] = {"host": request.host, "path": str(request.path)}
        except Exception:
            pass
        return data
