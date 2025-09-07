import plotly.express as px
from dash._utils import to_json
from aiocache import Cache
from flash_router import RootContainer, FlashRouter
from flash import Flash, State

from global_components.appshell import create_appshell
from theme import apply_vizro_theme
from concurrent.futures import ProcessPoolExecutor
import asyncio
import random


app = Flash(
    __name__,
    suppress_callback_exceptions=True,
    pages_folder="pages",
    use_pages=False,
    update_title=None,  # type: ignore[arg-type]
    routing_callback_inputs={"theme": State("color-scheme-toggle", "checked")},
    compress=True,
    router=FlashRouter,
    handle_theme=True,
)

app.layout = create_appshell([RootContainer()])
process_pool = ProcessPoolExecutor(max_workers=2)

server = app.server

import pandas as pd
import numpy as np

# Workload helpers
def make_df(size=100_000, seed=42):
    np.random.seed(seed)
    data = np.random.randn(size, 10)
    columns = [f"col{i}" for i in range(10)]
    return pd.DataFrame(data, columns=columns)

def workload_low():
    df = make_df(size=10_000, seed=random.randint(0, 10000))
    filtered = df[df["col0"] > 0]
    result = filtered["col1"].mean()
    return {"type": "low", "mean_col1": float(result)}

def workload_medium():
    df = make_df(size=50_000, seed=random.randint(0, 10000))
    df["group"] = np.random.choice(["A", "B", "C"], size=len(df))
    grouped = df.groupby("group")["col2"].sum().to_dict()
    return {"type": "medium", "group_sum_col2": grouped}

def workload_high():
    df1 = make_df(size=200_000, seed=random.randint(0, 10000))
    df2 = make_df(size=200_000, seed=random.randint(0, 10000))
    df2["key"] = np.random.randint(0, 5000, size=len(df2))
    df1["key"] = np.random.randint(0, 5000, size=len(df1))
    merged = pd.merge(df1, df2, on="key", suffixes=("_left", "_right"))
    count = len(merged)
    return {"type": "high", "merged_rows": count}

async def mock_db_request(timeout_range):
    timeout = random.uniform(*timeout_range)
    await asyncio.sleep(timeout)
    return {"db_timeout": round(timeout, 3)}

def pick_workload():
    # 2/3 chance for low/medium, 1/3 for high
    choice = random.choices(["low", "medium", "high"], weights=[1, 1, 1], k=1)[0]
    if choice == "low":
        return "low", workload_low()
    elif choice == "medium":
        return "medium", workload_medium()
    else:
        return "high", workload_high()

async def endpoint_logic():
    # DB timeout ranges by workload type
    timeout_ranges = {
        "low": (0.05, 0.2),      # 50-200ms
        "medium": (0.2, 0.6),   # 200-600ms
        "high": (0.6, 1.5),     # 600-1500ms
    }
    if random.random() < 2/3:
        workload_type, result = pick_workload()
        return {"status": "ok", **result}
    else:
        workload_type, result = pick_workload()
        db_result = await mock_db_request(timeout_ranges[workload_type])
        return {"status": "ok", **result, **db_result}


@app.server.get("/performance-check-1")
async def p1():
    return await endpoint_logic()


@app.server.get("/network-heavy-check")
async def network_heavy():
    delay = random.uniform(1.5, 3.5)
    await asyncio.sleep(delay)
    np.random.seed(random.randint(0, 10000))
    df = pd.DataFrame({
        "category": np.random.choice(["A", "B", "C", "D"], 40),
        "value1": np.random.randint(10, 100, 40),
        "value2": np.random.randn(40),
        "value3": np.random.uniform(0, 1, 40)
    })
    pivot = df.pivot_table(index="category", values=["value1", "value2", "value3"], aggfunc="mean").reset_index()
    fig = px.bar(pivot, x="category", y="value1", title="Mean Value1 by Category")
    fig_json = to_json(fig)
    return {
        "status": "ok",
        "network_delay": round(delay, 2),
        "pivot": pivot.to_dict(orient="records"),
        "plotly_fig": fig_json
    }

# router = FlashRouter(app)
cache = Cache()
apply_vizro_theme()
