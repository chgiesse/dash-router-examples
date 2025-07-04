from ..models import SalesCallbackParams

import dash_mantine_components as dmc


def create_sale_type_select(select_id: str = None, **kwargs):

    _id = {"id": select_id} if select_id else {}

    return dmc.Select(
        data=[
            {"value": val, "label": val.title()}
            for val in SalesCallbackParams.get_variants()
        ],
        placeholder="variant",
        size="sm",
        w=120,
        value=SalesCallbackParams.get_default_variant(),
        clearable=False,
        allowDeselect=False,
        variant="filled",
        comboboxProps={"transitionProps": {"transition": "fade-down", "duration": 200}},
        **_id,
        **kwargs
    )
