import random
from time import sleep
import pandas as pd


def get_row_data():
    sleep(random.random())
    df = pd.read_csv(
        "https://raw.githubusercontent.com/plotly/datasets/master/gapminder2007.csv"
    )
    return df
