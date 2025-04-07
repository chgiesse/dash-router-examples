from plotly.express import data
import dash_ag_grid as dag
import pandas as pd
import asyncio


async def get_data(chunk_size):
    df: pd.DataFrame = data.gapminder()
    total_rows = df.shape[0]

    while total_rows > 0:
        await asyncio.sleep(2)
        end = len(df) - total_rows + chunk_size
        total_rows -= chunk_size
        update_data = df[:end].to_dict("records")
        df.drop(df.index[:end], inplace=True)
        yield update_data, df.columns   