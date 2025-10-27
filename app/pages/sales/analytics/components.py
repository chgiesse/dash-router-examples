import dash_mantine_components as dmc
from datetime import date, datetime, timedelta
from flash import Input, Output, callback, State, set_props


class ActionSideBar(dmc.Stack):
    class ids:
        date_picker = "date-input-range-picker"
        multiselect = "multiselect-control"
        chipgroup = "chipgroup-multi"
        output = "output-div"

    def __init__(self):
        super().__init__(
            gap="lg",
            children=[
                dmc.DatePickerInput(
                    id=self.ids.date_picker,
                    label="Date Range",
                    description="Select a date range",
                    minDate=date(2020, 8, 5),
                    type="range",
                    value=[
                        datetime.now().date(),
                        datetime.now().date() + timedelta(days=5),
                    ],
                ),
                dmc.MultiSelect(
                    label="Control check icon",
                    placeholder="Select all you like!",
                    value=["Pandas", "TensorFlow"],
                    data=["Pandas", "NumPy", "TensorFlow", "PyTorch"],
                    checkIconPosition="right",
                    id=self.ids.multiselect,
                ),
                dmc.Group(
                    justify="flex-start",
                    gap="sm",
                    children=dmc.ChipGroup(
                        [
                            dmc.Chip("Multiple chips", value="a"),
                            dmc.Chip("Can be selected", value="b"),
                            dmc.Chip("At a time", value="c"),
                        ],
                        multiple=True,
                        value=["a", "b"],
                        id=self.ids.chipgroup,
                    ),
                ),
            ],
        )
