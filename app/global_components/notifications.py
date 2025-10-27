from dash import html
import dash_mantine_components as dmc
from flash import stream_props
# from dash_event_callback import stream_props as sync_stream_props
import random

class NotificationsContainer(dmc.Box):

    class ids:
        container = "notifications-container"
        notification = "default-notifixcation-id"

    @classmethod
    def send_notification(
        cls,
        title: str,
        message: str,
        id: str | None = None,
        color: str = "primary",
        autoClose=True,
        **kwargs,
    ):
        _id = id if id else random.randint(0, 1000)
        return stream_props(
            cls.ids.container,
            {
                "sendNotifications": [
                    dict(
                        title=title,
                        id=_id,
                        action="show",
                        message=message,
                        color=color,
                        autoClose=autoClose,
                        **kwargs,
                    )
                ]
            },
        )

    def __init__(self):
        super().__init__(
            [
                dmc.NotificationContainer(
                    id=self.ids.container,
                    transitionDuration=500,
                    position="top-right"
                ),
            ]
        )


class NotificationsContainerSync(html.Div):

    class ids:
        container = "notifications-container"

    @classmethod
    def push_notification(
        cls,
        title: str,
        message: str,
        id: str | None = None,
        color: str = "primary",
        autoClose=True,
        **kwargs,
    ):
        _id = id if id else random.randint(0, 1000)
        return stream_props(
            cls.ids.container,
            {
                "sendNotifications": [
                    dict(
                        title=title,
                        id=_id,
                        action="show",
                        message=message,
                        color=color,
                        autoClose=autoClose,
                        **kwargs,
                    )
                ]
            },
        )

    def __init__(self):
        super().__init__(
            children=[
                dmc.NotificationProvider(position="top-right", limit=2),
                html.Div(id=self.ids.container),
            ]
        )
