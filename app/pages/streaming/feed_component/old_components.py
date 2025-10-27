"""
OLD IMPLEMENTATION: Using callback outputs instead of set_props
This file recreates the same functionality as components.py but using traditional
Dash callback outputs instead of the newer set_props/stream_props approach.
Refactored to remove class structures for simpler function-based components.
"""

from .api import (
    load_users,
    add_user_to_json,
    delete_user_from_json,
    update_user,
    User
)
from .validation_helpers import parse_validation_errors
from pydantic import ValidationError

import dash_mantine_components as dmc
from typing import Dict, List
import random
import asyncio
from flash import (
    Patch,
    Input,
    State,
    Output,
    callback,
    event_callback,
    ALL,
    ctx,
    no_update,
)


def get_initials(name: str) -> str:
    parts = name.split()
    if len(parts) >= 2:
        return (parts[0][0] + parts[1][0]).upper()
    elif len(parts) == 1:
        return parts[0][0].upper()
    return ""


def create_notification(title: str, message: str, color: str = "primary", autoClose=True):
    """Helper to create notification dict"""
    return dict(
        title=title,
        id=random.randint(0, 1000),
        action="show",
        message=message,
        color=color,
        autoClose=autoClose,
    )


def notifications_container():
    return dmc.NotificationContainer(
        id="notifications-container",
        transitionDuration=500,
        position="bottom-right"
    )


def feed_component():
    return dmc.Stack(id="feed-component-container", children=dmc.Loader(m="auto"))


def user_form():
    return dmc.Stack(
        children=[
            dmc.TextInput(label="Name", id="user-name-field", placeholder="Enter your name"),
            dmc.TextInput(label="Email", id="user-email-field", placeholder="Enter your email"),
            dmc.Button("Submit", id="user-submit-button")
        ]
    )


def user_modal():
    return dmc.Group(
        [
            dmc.Modal(
                user_form(),
                id="user-modal",
                opened=False,
                title="User Management",
            ),
            dmc.Text("User Management", fw="bold", fz="lg", mr="auto"),
            dmc.Button("Add User", id="open-user-modal-button", variant="outline", disabled=True),
        ],
    )


def delete_modal():
    return dmc.Modal(
        [
            dmc.Text(
                "Are you sure you want to delete this user? This action cannot be undone."
            ),
            dmc.Text("Enter the user name to confirm.", c="dimmed"),
            dmc.Group([
                dmc.TextInput(id="del-modal-user-name-input", my="sm", flex=1),
                dmc.Button("Delete", id="confirm-delete-button", color="red", disabled=True)
            ]),
        ],
        id="delete-confirmation-modal",
        opened=False,
        title="Confirm Deletion",
    )


def user_card(user_data: User):
    return dmc.Card(
        id={"user_id": user_data.id, "type": "user-card"},
        className="fade-in-right",
        children=dmc.Group(
            [
                dmc.Avatar(get_initials(user_data.name), radius="xl"),
                dmc.Stack(
                    [
                        dmc.Text(user_data.name, fw="bold", fz="md"),
                        dmc.Text(user_data.email, fz="sm", c="gray"),
                    ],
                    gap=0
                ),
                dmc.Button(
                    "Delete",
                    id={"user_id": user_data.id, "type": "delete-user-btn"},
                    color="red",
                    variant="light",
                    size="xs",
                    ml="auto",
                    **{"data-user-name": user_data.name}
                ),
                dmc.Button(
                    "Edit",
                    id={"user_id": user_data.id, "type": "edit-user-btn"},
                    color="blue",
                    variant="light",
                    size="xs",
                    **{"data-user-name": user_data.name, "data-user-email": user_data.email}
                ),
            ],
        )
    )




# Callbacks

@callback(
    Output("feed-component-container", "children"),
    Output("user-modal", "opened", allow_duplicate=True),
    Output("user-name-field", "value", allow_duplicate=True),
    Output("user-email-field", "value", allow_duplicate=True),
    Output("user-submit-button", "user-edit-mode", allow_duplicate=True),
    Output("user-name-field", "error", allow_duplicate=True),
    Output("user-email-field", "error", allow_duplicate=True),
    Output("notifications-container", "sendNotifications", allow_duplicate=True),
    Input("user-submit-button", "n_clicks"),
    State("user-submit-button", "user-edit-mode"),
    State("user-name-field", "value"),
    State("user-email-field", "value"),
    running=[(Output("user-submit-button", "loading"), True, False)],
    prevent_initial_call=True,
)
async def store_user(
    _,
    edit_data: Dict[str, int],
    name: str,
    email: str
):
    # Validate using Pydantic model
    try:
        User(name=name, email=email)
    except ValidationError as e:
        errors_dict = parse_validation_errors(e, User)
        name_error = errors_dict.get("name")
        email_error = errors_dict.get("email")
        return no_update, no_update, no_update, no_update, no_update, name_error, email_error, no_update
    except Exception as e:
        # Handle any other unexpected errors
        notification = [create_notification(
            title="Error",
            message=str(e),
            color="red"
        )]
        return no_update, no_update, no_update, no_update, no_update, None, None, notification

    await asyncio.sleep(1)

    patch = Patch()
    notification = None

    if edit_data:
        edit_id = edit_data["user_id"]
        edit_index = edit_data["index"]
        updated = update_user(edit_id, name.strip(), email.strip())
        if not updated:
            notification = [create_notification(
                title="Error",
                message=f"Information for user {edit_id} could not be updated.",
                color="red"
            )]
            return no_update, no_update, no_update, no_update, no_update, None, None, notification

        # Update the card at the specific index
        patch[edit_index] = user_card(updated)
        notification = [create_notification(
            title="Success",
            message=f"{updated.name} information has been successfully updated.",
        )]
    else:
        user = add_user_to_json(name.strip(), email.strip())
        patch.append(user_card(user))
        notification = [create_notification(
            title="Success",
            message=f"{user.name} information has been successfully saved.",
        )]

    # Return: updated children, close modal, reset form fields, reset edit mode, clear errors, send notification
    return patch, False, "", "", None, None, None, notification


@callback(
    Output("user-modal", "opened"),
    Input("open-user-modal-button", "n_clicks"),
    prevent_initial_call=True,
)
def open_user_modal(_):
    return True


@callback(
    Output("user-name-field", "value"),
    Output("user-email-field", "value"),
    Output("user-submit-button", "user-edit-mode"),
    Output("user-name-field", "error"),
    Output("user-email-field", "error"),
    Input("user-modal", "opened"),
    prevent_initial_call=True,
)
def on_modal_closed(opened: bool):
    if not opened:
        # Reset form when modal closes
        return "", "", None, None, None
    return no_update, no_update, no_update, no_update, no_update


@callback(
    Output("delete-confirmation-modal", "opened", allow_duplicate=True),
    Output("del-modal-user-name-input", "placeholder"),
    Output("confirm-delete-button", "confirm-button-data"),
    Input({"type": "delete-user-btn", "user_id": ALL}, "n_clicks"),
    State({"type": "delete-user-btn", "user_id": ALL}, "data-user-name"),
    prevent_initial_call=True,
)
def init_delete(_, user_names: List[str]):
    triggered_id = ctx.triggered_id or {}
    user_id = triggered_id["user_id"]
    inputs = [x["id"] for x in ctx.inputs_list[-1]]
    idx = inputs.index(triggered_id)

    # Open modal with user data
    user_data = {"user_id": user_id, "index": idx}
    return True, user_names[idx], user_data


@callback(
    Output("feed-component-container", "children", allow_duplicate=True),
    Output("delete-confirmation-modal", "opened"),
    Output("del-modal-user-name-input", "value"),
    Output("del-modal-user-name-input", "placeholder", allow_duplicate=True),
    Output("confirm-delete-button", "disabled", allow_duplicate=True),
    Output("confirm-delete-button", "confirm-button-data", allow_duplicate=True),
    Output("notifications-container", "sendNotifications", allow_duplicate=True),
    Input("confirm-delete-button", "n_clicks"),
    State("confirm-delete-button", "confirm-button-data"),
    running=[(Output("confirm-delete-button", "loading"), True, False)],
    prevent_initial_call=True,
)
async def delete_user(_, user_data: Dict[str, int]):
    await asyncio.sleep(1)
    user_id = user_data["user_id"]
    idx = user_data["index"]

    deleted_user = delete_user_from_json(user_id)

    if not deleted_user:
        notification = [create_notification(
            title="Error",
            message="User could not be deleted.",
            color="red"
        )]
        return no_update, no_update, no_update, no_update, no_update, no_update, notification

    # Remove the card at the specific index
    patch = Patch()
    del patch[idx]

    notification = [create_notification(
        title="User Deleted",
        message=f"{deleted_user.name} has been successfully deleted.",
    )]

    # Return: updated children, close modal, reset name input, reset placeholder, disable button, reset button data, send notification
    return patch, False, "", "", True, None, notification


@callback(
    Output("confirm-delete-button", "disabled"),
    Input("del-modal-user-name-input", "value"),
    State("del-modal-user-name-input", "placeholder"),
    prevent_initial_call=True,
)
def validate_delete(name_input: str, user_name: str):
    if not user_name:
        return True

    is_match = name_input.strip().lower() == user_name.strip().lower()
    return not is_match


@callback(
    Output("user-name-field", "value", allow_duplicate=True),
    Output("user-email-field", "value", allow_duplicate=True),
    Output("user-submit-button", "user-edit-mode", allow_duplicate=True),
    Output("user-modal", "opened", allow_duplicate=True),
    Input({"type": "edit-user-btn", "user_id": ALL}, "n_clicks"),
    State({"type": "edit-user-btn", "user_id": ALL}, "data-user-name"),
    State({"type": "edit-user-btn", "user_id": ALL}, "data-user-email"),
    prevent_initial_call=True,
)
def edit_user(_, user_names: List[str], user_emails: List[str]):
    triggered_id = ctx.triggered_id or {}
    user_id = triggered_id["user_id"]
    inputs = [x["id"] for x in ctx.inputs_list[0]]
    idx = inputs.index(triggered_id)

    # Return: fill form with user data, set edit mode, open modal
    edit_data = {"user_id": user_id, "index": idx}
    return user_names[idx], user_emails[idx], edit_data, True


@event_callback(
    Output("feed-component-container", "children", allow_duplicate=True),
    Output("open-user-modal-button", "disabled"),
    Input("feed-component-container", "id"),
    prevent_initial_call=False,
)
async def load_feed(_):
    # First yield: clear container and enable button
    await asyncio.sleep(1)
    yield [], False

    # Load users and add them one by one
    users = load_users()
    patch = Patch()
    for user in users:
        await asyncio.sleep(0.2)
        card = user_card(user)
        patch.append(card)
        # Yield the growing list of cards and keep button enabled
        yield patch, False
