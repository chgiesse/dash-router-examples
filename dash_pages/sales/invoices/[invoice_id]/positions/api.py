from aiocache import cached
import random
from time import sleep


# @cached(ttl=30)
def endpoint(*args, **kwargs):
    sleep(0.3)
    data = [
        {"name": "USA", "value": random.randint(50, 3000), "color": "indigo.6"},
        {"name": "India", "value": random.randint(50, 3000), "color": "violet.5"},
        {"name": "Japan", "value": random.randint(50, 3000), "color": "violet.3"},
        {"name": "Other", "value": random.randint(50, 3000), "color": "gray.6"},
    ]
    return data
