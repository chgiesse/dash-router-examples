from dash import html


class LacyContainer(html.Div):
    class ids:
        container = lambda idx: {"index": idx, "type": "lacy-container"}

    def __init__(self, children, index, **kwargs):
        super().__init__(children, id=self.ids.container(index), **kwargs)
