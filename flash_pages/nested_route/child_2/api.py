import random
import asyncio
import pandas as pd


async def get_row_data():
    await asyncio.sleep(random.random())
    df = pd.read_csv(
        "https://raw.githubusercontent.com/plotly/datasets/master/gapminder2007.csv"
    )
    return df