from dash import html
import dash_mantine_components as dmc
# from streaming.stream import flash_props


class NotificationsContainer(html.Div):

    class ids:
        container = "notifications-container"

    # @classmethod
    # async def push_notification(cls, **kwargs):
    #     timer = kwargs.pop("autoClose", None) or 3000
    #     return await flash_props(
    #         cls.ids.container, {"children": dmc.Notification(**kwargs, autoClose=timer)}
    #     )

    # @classmethod
    # async def clean_notifications(cls, **kwargs):
    #     return await flash_props(
    #         cls.ids.container,
    #         {"children": dmc.Notification(action="cleanQueue", message="", **kwargs)},
    #     )

    def __init__(self):
        super().__init__(
            children=[
                dmc.NotificationProvider(position="top-right", limit=2),
                html.Div(id=self.ids.container),
            ]
        )
