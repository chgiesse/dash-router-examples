import dash_mantine_components as dmc
from dash_router import RootContainer
from dash import dcc

print('MODULE: ', __name__, flush=True)

layout = dmc.Center(dmc.Loader(type="dots"))