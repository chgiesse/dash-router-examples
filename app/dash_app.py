import plotly.express as px
from dash._utils import to_json


# ...existing code...

from global_components.appshell import create_appshell
from dash import Dash, State, html
from theme import apply_vizro_theme
from dash_router import RootContainer, Router
import time

app = Dash(
    __name__,
    suppress_callback_exceptions=True,
    routing_callback_inputs={"theme": State("color-scheme-toggle", "checked")},
    pages_folder="dash_pages"
)
server = app.server
router = Router(app, pages_folder="dash_pages")
apply_vizro_theme()

# Workload helpers


import pandas as pd
import numpy as np
import random

def make_df(size=100_000, seed=42):
    np.random.seed(seed)
    data = np.random.randn(size, 10)
    columns = [f"col{i}" for i in range(10)]
    return pd.DataFrame(data, columns=columns)

def workload_low():
    ("[PERF] Running LOW workload (10k rows)")
    df = make_df(size=10_000, seed=random.randint(0, 10000))
    filtered = df[df["col0"] > 0]
    result = filtered["col1"].mean()
    return {"type": "low", "mean_col1": float(result)}

def workload_medium():
    ("[PERF] Running MEDIUM workload (50k rows)")
    df = make_df(size=50_000, seed=random.randint(0, 10000))
    df["group"] = np.random.choice(["A", "B", "C"], size=len(df))
    grouped = df.groupby("group")["col2"].sum().to_dict()
    return {"type": "medium", "group_sum_col2": grouped}

def workload_high():
    ("[PERF] Running HIGH workload (200k rows, merge)")
    df1 = make_df(size=200_000, seed=random.randint(0, 10000))
    df2 = make_df(size=200_000, seed=random.randint(0, 10000))
    df2["key"] = np.random.randint(0, 5000, size=len(df2))
    df1["key"] = np.random.randint(0, 5000, size=len(df1))
    merged = pd.merge(df1, df2, on="key", suffixes=("_left", "_right"))
    count = len(merged)
    return {"type": "high", "merged_rows": count}

def mock_db_request(timeout_range):
    timeout = random.uniform(*timeout_range)
    (f"[PERF] Simulating sync DB request (timeout: {timeout:.3f}s, range: {timeout_range})")
    time.sleep(timeout)
    return {"db_timeout": round(timeout, 3)}

def pick_workload():
    choice = random.choices(["low", "medium", "high"], weights=[1, 1, 1], k=1)[0]
    (f"[PERF] Workload choice: {choice.upper()}")
    if choice == "low":
        return "low", workload_low()
    elif choice == "medium":
        return "medium", workload_medium()
    else:
        return "high", workload_high()

def endpoint_logic():
    timeout_ranges = {
        "low": (0.05, 0.2),      # 50-200ms
        "medium": (0.2, 0.6),   # 200-600ms
        "high": (0.6, 1.5),     # 600-1500ms
    }
    if random.random() < 2/3:
        ("[PERF] Running only workload (no DB mock)")
        workload_type, result = pick_workload()
        return {"status": "ok", **result}
    else:
        ("[PERF] Running workload + DB mock")
        workload_type, result = pick_workload()
        db_result = mock_db_request(timeout_ranges[workload_type])
        return {"status": "ok", **result, **db_result}

@app.server.get("/performance-check-1")
def p1():
    return endpoint_logic()

@app.server.get("/network-heavy-check")
def network_heavy():
    ("[PERF] Simulating long network-bound request (sync)")
    # Simulate network delay (1.5-3.5s)
    delay = random.uniform(1.5, 3.5)
    time.sleep(delay)
    (f"[PERF] Network delay: {delay:.2f}s")
    # Create small DataFrame
    np.random.seed(random.randint(0, 10000))
    df = pd.DataFrame({
        "category": np.random.choice(["A", "B", "C", "D"], 40),
        "value1": np.random.randint(10, 100, 40),
        "value2": np.random.randn(40),
        "value3": np.random.uniform(0, 1, 40)
    })
    pivot = df.pivot_table(index="category", values=["value1", "value2", "value3"], aggfunc="mean").reset_index()
    ("[PERF] Pivoted DataFrame:")
    # Create Plotly chart
    fig = px.bar(pivot, x="category", y="value1", title="Mean Value1 by Category")
    fig_json = to_json(fig)
    return {
        "status": "ok",
        "network_delay": round(delay, 2),
        "pivot": pivot.to_dict(orient="records"),
        "plotly_fig": fig_json
    }

app.layout = create_appshell([RootContainer()])

if __name__ == "__main__":
    app.run(debug=True, port=8000)
