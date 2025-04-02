from plotly.express import data
import dash_ag_grid as dag
import pandas as pd
import asyncio


async def get_data():
    df: pd.DataFrame = data.gapminder()
    rows_per_step = 500
    total_rows = df.shape[0]

    while total_rows > 0:
        await asyncio.sleep(2)
        end = len(df) - total_rows + rows_per_step
        total_rows -= rows_per_step
        update_data = df[:end].to_dict("records")
        df.drop(df.index[:end], inplace=True)
        yield update_data, df.columns   