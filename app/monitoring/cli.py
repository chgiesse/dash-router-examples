from __future__ import annotations

import argparse
import asyncio
import json
import os
from contextlib import suppress
from dataclasses import dataclass
from typing import Optional

import httpx
from rich import box
from rich.align import Align
from rich.columns import Columns
from rich.console import Console
from rich.live import Live
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.rule import Rule
from collections import deque


def _fmt_bytes(n: int | float) -> str:
    value = float(n)
    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if value < 1024:
            return f"{value:.0f} {unit}"
        value /= 1024
    return f"{value:.0f} PB"


async def fetch_metrics(base_url: str, client: httpx.AsyncClient):
    url = base_url.rstrip("/") + "/__metrics"
    r = await client.get(url, timeout=3.0)
    r.raise_for_status()
    return r.json()


def _sparkline(values: list[float], width: int = 40) -> Text:
    blocks = "▁▂▃▄▅▆▇█"
    if not values:
        return Text("".ljust(width))
    vals = values[-width:]
    vmax = max(vals) or 1.0
    out = Text()
    for v in vals:
        idx = int((v / vmax) * (len(blocks) - 1))
        color = "green" if v < 0.5 * vmax else ("yellow" if v < 0.8 * vmax else "red")
        out.append(blocks[idx], style=color)
    return out


def _bar(value: float, max_value: float, width: int = 18, color: str = "cyan") -> Text:
    if max_value <= 0:
        return Text()
    ratio = max(0.0, min(1.0, value / max_value))
    filled = int(ratio * width)
    return Text("█" * filled, style=color) + Text("░" * (width - filled), style="grey37")


def _status_color(code: int) -> str:
    if 200 <= code < 300:
        return "green"
    if 300 <= code < 400:
        return "cyan"
    if 400 <= code < 500:
        return "yellow"
    return "red"


def render_view(d: dict, rps: float, rps_hist: list[float], err_rate: float) -> Panel:
    req = d.get("requests", {})
    lat = d.get("latency_s", {})
    streams = d.get("streams", {})
    proc = d.get("process", {})
    server = d.get("server", {})

    # Header
    title = Text("⚡ Dash/Quart Monitor", style="bold cyan")
    subtitle = Text(f" {server.get('host','')} • Uptime {d.get('uptime_s',0):.0f}s", style="dim")

    # KPIs left
    kpi = Table.grid(padding=(0, 1))
    kpi.add_column(justify="right")
    kpi.add_column(justify="left")
    kpi.add_row("Requests", f"[bold]{req.get('total',0)}[/bold]")
    kpi.add_row("In-Flight", f"{req.get('in_flight',0)}")
    kpi.add_row("Exceptions", f"[red]{req.get('exceptions',0)}[/red]")
    kpi.add_row("RPS", f"[bold]{rps:.2f}[/bold]")
    kpi.add_row("Error rate", f"[red]{err_rate:.2%}[/red]" if err_rate else "0.00%")
    kpi.add_row("Latency avg", f"{lat.get('avg',0)*1000:.1f} ms")
    kpi.add_row("Latency p90", f"{lat.get('p90',0)*1000:.1f} ms")
    kpi.add_row("Latency p99", f"{lat.get('p99',0)*1000:.1f} ms")

    # Streams/Process right
    sys = Table.grid(padding=(0, 1))
    sys.add_column(justify="right")
    sys.add_column(justify="left")
    sys.add_row("SSE in-flight", f"{streams.get('sse_in_flight',0)}")
    sys.add_row("WS connections", f"{streams.get('ws_connections',0)}")
    sys.add_row("CPU %", f"{proc.get('cpu_percent',0):.1f}")
    rss = proc.get("rss_bytes", 0) or 0
    sys.add_row("RSS", _fmt_bytes(rss))
    sys.add_row("Threads", f"{proc.get('threads',0)}")

    # Status table with colors
    st = Table(title="Status Codes", box=box.ROUNDED, expand=True, show_edge=False)
    st.add_column("Code", justify="right")
    st.add_column("Count", justify="right")
    for code, count in sorted((req.get("by_status") or {}).items()):
        st.add_row(f"[{_status_color(int(code))}]{code}[/]", f"{count}")

    # Path table with bars
    path_counts = sorted((req.get("by_path_group") or {}).items(), key=lambda x: x[1], reverse=True)[:10]
    max_path = max([c for _, c in path_counts], default=0)
    pt = Table(title="Top Paths", box=box.ROUNDED, expand=True, show_edge=False)
    pt.add_column("Path Group")
    pt.add_column("Count", justify="right")
    pt.add_column("Load", justify="left")
    for path, count in path_counts:
        pt.add_row(path, str(count), _bar(count, max_path, color="magenta"))

    # RPS sparkline row
    spark = _sparkline(rps_hist, width=50)
    spark_panel = Panel(Align.left(Text("Requests/s ") + spark), box=box.SQUARE, border_style="blue")

    # Compose layout
    header = Table.grid(expand=True)
    header.add_column(ratio=1)
    header.add_column(justify="right")
    header.add_row(title, subtitle)

    top = Columns([
        Panel(kpi, title="Throughput & Latency", border_style="cyan", box=box.ROUNDED),
        Panel(sys, title="Streams & System", border_style="cyan", box=box.ROUNDED),
    ])

    body = Columns([
        st,
        pt,
    ])

    grid = Table.grid(expand=True)
    grid.add_row(header)
    grid.add_row(spark_panel)
    grid.add_row(top)
    grid.add_row(body)

    return Panel(grid, border_style="cyan")


async def _run_top(url: str, interval: float) -> None:
    console = Console()
    rps_hist: deque[float] = deque(maxlen=200)
    prev_total = None
    prev_time = None
    prev_status = {}
    async with httpx.AsyncClient() as client:
        with Live(Panel(Text("Connecting...")), console=console, refresh_per_second=8) as live:
            while True:
                try:
                    data = await fetch_metrics(url, client)
                    # compute RPS and error rate deltas
                    import time
                    now = time.time()
                    total = data.get("requests", {}).get("total", 0) or 0
                    by_status = (data.get("requests", {}).get("by_status") or {}).copy()
                    if prev_total is not None and prev_time is not None:
                        dt = max(1e-6, now - prev_time)
                        rps = max(0.0, (total - prev_total) / dt)
                        rps_hist.append(rps)
                        # error rate: 5xx in delta / total delta
                        delta_total = max(0, total - prev_total)
                        delta_5xx = 0
                        for code, count in by_status.items():
                            if int(code) >= 500:
                                prev_c = int(prev_status.get(code, 0))
                                delta_5xx += max(0, int(count) - prev_c)
                        err_rate = (delta_5xx / delta_total) if delta_total else 0.0
                    else:
                        rps = 0.0
                        err_rate = 0.0
                        rps_hist.append(0.0)

                    prev_total = total
                    prev_time = now
                    prev_status = by_status

                    live.update(render_view(data, rps, list(rps_hist), err_rate))
                except Exception as e:
                    live.update(Panel(Text(f"Error: {e}", style="red"), title="dash-monitor"))
                await asyncio.sleep(interval)


def main():  # console_script entrypoint
    parser = argparse.ArgumentParser(prog="dash-monitor", description="Monitor a Dash/Quart app")
    parser.add_argument("command", nargs="?", default="top", help="Command (only 'top' supported)")
    parser.add_argument("url", nargs="?", default="http://127.0.0.1:8050", help="Base URL of your app")
    parser.add_argument("--interval", "-i", type=float, default=1.0, help="Refresh seconds")
    args = parser.parse_args()

    if args.command not in ("top",):
        print("Unknown command. Use: top")
        raise SystemExit(2)

    asyncio.run(_run_top(args.url, args.interval))


if __name__ == "__main__":
    main()
