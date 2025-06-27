from datetime import date

import dash_dynamic_grid_layout as dgl
import dash_mantine_components as dmc
from dash_iconify import DashIconify
from dash_router import RootContainer, SlotContainer
from dash_router.utils.helper_functions import recursive_to_plotly_json
from dash import Input, Output, State, clientside_callback

from .models import QueryParams


class ActionBar(dmc.Stack):
    class ids:
        filter_collapse = "db-filter-collapse"
        veggie_select = "veggie-select"
        country_select = "country-select"
        period_selext = "period-select"
        show_filter_button = "fb-show-filter-button"
        edit_button = "db-edit-button"
        filter_button = "fb-filter-button"
        filter_icon = "db-filter-icon"

    toggle_collapse_csc = clientside_callback(
        f"""
        //js
        function ( nClicks, opened ) {{
            if ( nClicks === undefined) {{
                return window.dash_clientside.no_update
            }}

            const nextOpen = !opened
            const rotateAmount = opened ? 0 : 2
            window.dash_clientside.set_props('{ids.filter_icon}', {{rotate: rotateAmount}})
            return nextOpen
        }}
        ;//
        """,
        Output(ids.filter_collapse, "opened"),
        Input(ids.show_filter_button, "n_clicks"),
        State(ids.filter_collapse, "opened"),
    )

    update_url_csc = clientside_callback(
        f""" 
        function(country, period, veggie, currentPath, currentSearch ) {{
            // Create a new URLSearchParams object
            const queryParams = new URLSearchParams();
            const noUpdate = window.dash_clientside.no_update
            // Add parameters if they have values
            if (country) queryParams.set('country', country);

            if (period) {{
                if (Array.isArray(period) && period.some((el) => el === null)) {{
                    console.log('Date is not complete');
                    return noUpdate
                }};
                if (period.length == 2 && period.every((el) => el !== null)) {{
                    queryParams.set('period', period.join(', '))
                }};
                
            }};
            if (veggie) queryParams.set('veggie', veggie);
            
            // Create the new URL string
            const queryString = queryParams.toString();
            
            // Return the updated URL
            window.dash_clientside.set_props('{ids.filter_button}', {{href: currentPath + '?' + queryString}})
            // return noUpdate
            // if (queryParams) {{
            //     return queryString
            // }}

        }}
        """,
        Input(ids.country_select, "value"),
        Input(ids.period_selext, "value"),
        Input(ids.veggie_select, "value"),
        State(RootContainer.ids.location, "pathname"),
        State(RootContainer.ids.location, "search"),
        prevent_initial_call=True,
    )

    def __init__(self, filter_params: QueryParams):
        opened = not filter_params.is_empty
        rotate = 2 if opened else 0

        super().__init__(
            mb="md",
            children=[
                dmc.Group(
                    [
                        dmc.Anchor(
                            dmc.Badge(
                                "Go Back",
                                variant="outline",
                                className="badge-btn",
                                leftSection=DashIconify(
                                    icon="icons8:left-round", height=16
                                ).to_plotly_json(),
                            ),
                            href="/nested-route",
                        ),
                        dmc.Button(
                            children="Edit",
                            rightSection=DashIconify(
                                icon="clarity:settings-line", width=15
                            ).to_plotly_json(),
                            variant="filled",
                            id=self.ids.edit_button,
                            ml="auto",
                            w=100,
                            justify="space-between",
                        ),
                        dmc.Button(
                            children="Filter",
                            rightSection=DashIconify(
                                icon="ep:arrow-down",
                                width=15,
                                id=self.ids.filter_icon,
                                rotate=rotate,
                            ).to_plotly_json(),
                            variant="light",
                            id=self.ids.show_filter_button,
                            w=100,
                            justify="space-between",
                        ),
                    ]
                ),
                dmc.Collapse(
                    opened=opened,
                    id=self.ids.filter_collapse,
                    animateOpacity=True,
                    transitionDuration=200,
                    transitionTimingFunction="linear",
                    children=dmc.Flex(
                        flex=1,
                        direction="row",
                        gap="sm",
                        children=[
                            dmc.Select(
                                id=self.ids.veggie_select,
                                placeholder="Remove Veggie",
                                value=filter_params.veggie,
                                style={"flex": "1 1 auto"},
                                leftSection=DashIconify(
                                    icon="ph:dot-outline", height=20
                                ).to_plotly_json(),
                                clearable=True,
                                comboboxProps={
                                    "transitionProps": {
                                        "transition": "pop",
                                        "duration": 200,
                                    }
                                },
                                data=[
                                    {"value": value, "label": value.title()}
                                    for value in filter_params.get_literals("veggie")
                                ],
                            ),
                            dmc.Select(
                                id=self.ids.country_select,
                                placeholder="Remove Country",
                                value=filter_params.country,
                                leftSection=DashIconify(
                                    icon="ph:dot-outline", height=20
                                ).to_plotly_json(),
                                style={"flex": "1 1 auto"},
                                clearable=True,
                                comboboxProps={
                                    "transitionProps": {
                                        "transition": "pop",
                                        "duration": 200,
                                    }
                                },
                                data=[
                                    {"value": value, "label": value.title()}
                                    for value in filter_params.get_literals("country")
                                ],
                            ),
                            dmc.DatePickerInput(
                                id=self.ids.period_selext,
                                minDate=date(2020, 8, 5),
                                value=filter_params.period,
                                type="range",
                                placeholder="Pick dates",
                                clearable=True,
                                valueFormat="YYYY-MM-DD",
                                dropdownType="modal",
                                numberOfColumns=2,
                                style={"flex": "1 1 auto"},
                                miw=200,
                                leftSection=DashIconify(
                                    icon="ph:dot-outline", height=20
                                ).to_plotly_json(),
                            ),
                            dmc.Anchor(
                                children=dmc.ActionIcon(
                                    DashIconify(icon="prime:filter", height=20),
                                    size="lg",
                                    variant="subtle",
                                ),
                                id=self.ids.filter_button,
                                href="/nested-route/child-3",
                                style={"flex": "0 0 auto"},
                            ),
                        ],
                    ),
                ),
                dmc.Divider(),
            ],
        )


class ResizeGrid(dgl.DashGridLayout):
    class ids:
        grid = "resize-grid-layout"

    toggle_edit_csc = clientside_callback(
        f"""function( nClicks, resize ){{
            const buttonText = resize ? 'Edit' : 'Save';
            window.dash_clientside.set_props(
                '{ActionBar.ids.edit_button}', 
                {{children: buttonText}}
            );
            return !resize
        }}""",
        Output(ids.grid, "showResizeHandles"),
        Input(ActionBar.ids.edit_button, "n_clicks"),
        State(ids.grid, "showResizeHandles"),
        prevent_initial_call=True,
    )

    def __init__(self, slot_1: SlotContainer, slot_2: SlotContainer):
        super().__init__(
            id=self.ids.grid,
            showResizeHandles=False,
            itemLayout=[
                dict(w=3, h=4, x=0, y=0, i="0"),
                dict(w=3, h=4, x=3, y=0, i="1"),
            ],
            items=[
                dgl.DraggableWrapper(recursive_to_plotly_json(slot_1)).to_plotly_json(),
                dgl.DraggableWrapper(recursive_to_plotly_json(slot_2)).to_plotly_json(),
            ],
            rowHeight=75,
            cols={"lg": 12, "md": 10, "sm": 6, "xs": 4, "xxs": 2},
            showRemoveButton=False,
        )
