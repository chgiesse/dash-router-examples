# from .components.actionbar import ActionBar
# from .components.menu import GraphDownload
# from .models import AmazonQueryParams

# import dash_mantine_components as dmc


# def layout(
#     ranks=None, 
#     revenue=None, 
#     sentiment=None, 
#     filters: AmazonQueryParams = None, 
#     **kwargs
# ):

#     filters = AmazonQueryParams(**kwargs)

#     return [
#         GraphDownload(),
#         dmc.Grid(
#             children=[
#                 dmc.GridCol(
#                     span=9,
#                     children=dmc.Grid(
#                         [
#                             dmc.GridCol(
#                                 ranks,
#                                 span=12 if filters.is_single_view else 4,
#                             ),
#                             dmc.GridCol(
#                                 revenue,
#                                 span=12 if filters.is_single_view else 8,
#                             ),
#                             dmc.GridCol(
#                                 sentiment,
#                                 span=12,
#                             ),
#                         ]
#                     ),
#                 ),
#                 dmc.GridCol(
#                     span=3,
#                     pos="sticky",
#                     top=0,
#                     h="calc(100vh - var(--mantine-spacing-xl))",
#                     bg="var(--mantine-color-body)",
#                     children=[
#                         dmc.Title("Example Dashboard", order=2, ml="md"),
#                         ActionBar(filters),
#                     ],
#                 ),
#             ]
#         ),
#     ]
