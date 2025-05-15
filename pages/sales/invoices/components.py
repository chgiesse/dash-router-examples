import dash_mantine_components as dmc
from utils.helpers import get_icon


def create_a_button(href: str):
    return dmc.Anchor(
        children=dmc.Button(
            "Open",
            variant="light",
            size="compact-sm",
            rightSection=get_icon("material-symbols:open-in-new").to_plotly_json(),
        ).to_plotly_json(),
        underline=False,
        href=href,
    ).to_plotly_json()


def create_td_skeleton():
    return dmc.Skeleton(height="1.2rem", my="0.3rem").to_plotly_json()


def create_invoice_table(data=[], is_loading: bool = False):
    data = data or [{} for _ in range(0, 5)]
    rows = [
        dmc.TableTr(
            [
                dmc.TableTd(
                    (
                        element.get("invoice_id")
                        if not is_loading
                        else create_td_skeleton()
                    ),
                    w="15%",
                ),
                dmc.TableTd(
                    element.get("mass") if not is_loading else create_td_skeleton(),
                    w="30%",
                ),
                dmc.TableTd(
                    element.get("symbol") if not is_loading else create_td_skeleton(),
                    w="20%",
                ),
                dmc.TableTd(
                    element.get("amount") if not is_loading else create_td_skeleton(),
                    w="fit-content",
                ),
                dmc.TableTd(
                    (
                        create_a_button(element.get("action"))
                        if not is_loading
                        else create_td_skeleton()
                    ),
                    w="20%",
                ),
            ]
        )
        for element in data
    ]
    body = dmc.TableTbody(rows)
    head = dmc.TableThead(
        dmc.TableTr(
            [
                dmc.TableTh("Invoice ID"),
                dmc.TableTh("Vendor"),
                dmc.TableTh("Issued Date"),
                dmc.TableTh("Amount"),
                dmc.TableTh("Action"),
            ]
        )
    )

    return dmc.Table(
        [head, body],
        verticalSpacing="sm",
        horizontalSpacing="sm",
        highlightOnHover=True,
        withTableBorder=False,
        withColumnBorders=False,
        withRowBorders=False,
    )
