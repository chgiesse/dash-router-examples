import dash_mantine_components as dmc
from utils.helpers import get_icon
from flash import clientside_callback, Input, Output, State
from dash_router import RootContainer


def create_td_skeleton():
    return dmc.Skeleton(height="1rem").to_plotly_json()


def create_invoice_table(data = [], page: int = 1,  is_loading: bool = False):

    def create_a_button(href: str):
        return dmc.Anchor(
            children=dmc.Button(
                "Open",
                variant="light",
                size="compact-sm",
                rightSection=get_icon("material-symbols:open-in-new").to_plotly_json(),
            ).to_plotly_json(),
            underline=False,
            href=(href + "?page=" + str(page) if page else href),
        ).to_plotly_json()

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
            ],
            h=50
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
        className="fade-in-chart",
        h=300
    )


class InvoicePagination(dmc.Pagination):
    class ids:
        pagination = 'invoice-pagination'
    
    clientside_callback(
        """
        function(page, current_search) {
            // Parse current URL parameters
            const urlParams = new URLSearchParams(current_search || '');
            
            // Update or add the page parameter
            if (page) {
                urlParams.set('page', page.toString());
            } else {
                // Remove page parameter if page is 1 or falsy
                urlParams.delete('page');
            }
            
            // Return the updated query string
            const newSearch = urlParams.toString();
            return newSearch ? '?' + newSearch : '';
        }
        """,
        Output(RootContainer.ids.location, "search"),
        Input(ids.pagination, "value"),
        State(RootContainer.ids.location, "search"),
        prevent_initial_call=True
    )
    
    def __init__(self, page: int = 1):
        super().__init__(
            id=self.ids.pagination,
            total=5,
            withControls=False,
            value=page,
        )