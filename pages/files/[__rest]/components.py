from functools import reduce
from typing import List
import dash_mantine_components as dmc


def create_route_bar(route_elements: List[str]):
    def create_anchor_reducer(acc, element):
        # acc is a tuple of (list_of_anchors, current_path)
        anchors, current_path = acc

        # Create new path
        new_path = f"{current_path}/{element}"

        # Add new anchor to the list
        anchors.append(dmc.Anchor(element.title(), href=new_path, underline=True))

        # Return updated accumulator
        return (anchors, new_path)

    # Initial state: list with 'Files' anchor and current path 'files'
    initial_state = ([dmc.Anchor("Files", href="/files", underline=False)], "/files")

    # Apply reduction and return just the list of anchors
    anchors, _ = reduce(create_anchor_reducer, route_elements, initial_state)
    return dmc.Breadcrumbs(anchors)
