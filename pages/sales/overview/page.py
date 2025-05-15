import dash_mantine_components as dmc
from dash_router import RouteConfig
from dash import dcc

from .._components.lacy import LacyTestComponent

config = RouteConfig(path_template="<...rest>")


async def layout(**kwargs):
    # def layout(**kwargs):
    return dcc.Markdown(
        """
        # Flash Roadmap

        ## Phase 1 
        * Flash 1.0.0 (merge latest Dash 3.0.1 updates)
        * _finished this month_

        ## Phase 2
        * Flash / Dash router 
        * _finished next month_ 

        ## Phase 3 
        * Add native SSE callback to replace background callback 
        * cpu bound callback
        * _Target: Q2_

        ## Phase 4 
        * Add native WS callback and broadcasting 
        * bring back background callbackmanager 
        * _Target: Q2_
        """
    )
