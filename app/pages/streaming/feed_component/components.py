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
    set_props,
    callback,
    event_callback,
    stream_props,
    ALL,
    ctx,
)


def get_initials(name: str) -> str:
    parts = name.split()
    if len(parts) >= 2:
        return (parts[0][0] + parts[1][0]).upper()
    elif len(parts) == 1:
        return parts[0][0].upper()
    return ""


class NotificationsContainer(dmc.NotificationContainer):

    class ids:
        container = "notifications-container"
        notification = "default-notification-id"

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
        set_props(
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
                        position="bottom-center",
                        **kwargs,
                    )
                ]
            },
        )

    def __init__(self):
        super().__init__(
            id=self.ids.container,
            transitionDuration=500,
            position="bottom-center"
        )


class FeedComponent(dmc.Stack):

    class ids:
        container = "feed-component-container"

    @classmethod
    def add_child(cls, child, stream: bool = False, prepend: bool = False):
        patch = Patch()
        patch.append(child) if not prepend else patch.prepend(child)
        if stream:
            return stream_props(cls.ids.container, {"children": patch})

        set_props(cls.ids.container, {"children": patch})

    @classmethod
    def remove_child(cls, child_index: int, stream: bool = False):
        patch = Patch()
        del patch[child_index]
        if stream:
            return stream_props(cls.ids.container, {"children": patch})

        set_props(cls.ids.container, {"children": patch})

    def __init__(self):
        super().__init__(id=self.ids.container, children=dmc.Loader(m="auto"))


class UserForm(dmc.Stack):

    class ids:
        name_field = "user-name-field"
        email_field = "user-email-field"
        submit_button = "user-submit-button"
        edit_data = "data-user-data"  # custom prop to track edit mode

    callback_inputs = [
        Input(ids.submit_button, "n_clicks"),
        State(ids.submit_button, ids.edit_data),
        State(ids.name_field, "value"),
        State(ids.email_field, "value"),
    ]

    @classmethod
    def set_edit_mode(cls, user_id: int | None, index: int | None = None):
        data = (
            {"user_id": user_id, "index": index}
            if index is not None
            else None
        )
        set_props(cls.ids.submit_button, {cls.ids.edit_data: data})

    @classmethod
    def set_error_state(cls, name_error: str | None = None, email_error: str | None = None):
        set_props(cls.ids.name_field, {"error": name_error})
        set_props(cls.ids.email_field, {"error": email_error})

    def __init__(self, name: str = "", email: str = "", edit_data: Dict[str, int] | None = None):
        super().__init__(
            children=[
                dmc.TextInput(label="Name", id=self.ids.name_field, placeholder="Enter your name", value=name),
                dmc.TextInput(label="Email", id=self.ids.email_field, placeholder="Enter your email", value=email),
                dmc.Button("Submit", id=self.ids.submit_button, **{self.ids.edit_data: edit_data} if edit_data else {})
            ]
        )


class DeleteForm(dmc.Stack):

    class ids:
        name_input = "delete-form-name-input"
        confirm_button = "delete-form-confirm-button"
        button_data = "data-delete-user"

    @classmethod
    def set_button_disabled(cls, disabled: bool):
        set_props(cls.ids.confirm_button, {"disabled": disabled})

    def __init__(self, user_name: str = "", user_id: int | None = None, index: int | None = None):
        delete_data = {"user_id": user_id, "index": index} if user_id is not None and index is not None else {}
        super().__init__(
            children=[
                dmc.Text(
                    "Are you sure you want to delete this user? This action cannot be undone."
                ),
                dmc.Text("Enter the user name to confirm.", c="dimmed"),
                dmc.Group([
                    dmc.TextInput(id=self.ids.name_input, my="sm", flex=1, placeholder=user_name),
                    dmc.Button(
                        "Delete",
                        id=self.ids.confirm_button,
                        color="red",
                        disabled=True,
                        **{self.ids.button_data: delete_data}
                    )
                ]),
            ]
        )


class UserModal(dmc.Group):

    class ids:
        modal = "user-modal"
        open_button = "open-user-modal-button"

    @classmethod
    def close(cls):
        cls.reset()
        set_props(cls.ids.modal, {"opened": False})

    @classmethod
    def open(cls, form, title: str = "User Management"):
        set_props(cls.ids.modal, {"children": form, "opened": True, "title": title})

    @classmethod
    def reset(cls):
        set_props(cls.ids.modal, {"children": None})

    def __init__(self) -> None:
        super().__init__(
            [
                dmc.Modal(
                    id=self.ids.modal,
                    opened=False,
                    title="User Management",
                ),
                dmc.Text("User Management", fw="bold", fz="lg", mr="auto"),
                dmc.Button("Add User", id=self.ids.open_button, variant="outline", disabled=True),
            ],
        )


class UserCard(dmc.Card):

    class ids:
        delete_btn = lambda user_id: {"user_id": user_id, "type": "delete-user-btn"}
        card = lambda user_id: {"user_id": user_id, "type": "user-card"}
        edit_btn = lambda user_id: {"user_id": user_id, "type": "edit-user-btn"}

    @classmethod
    def update(cls, user_data: User, card_idx: int):
        patch = Patch()
        new_card = cls(user_data)
        patch[card_idx] = new_card
        set_props(FeedComponent.ids.container, {"children": patch})


    def __init__(self, user_data: User) -> None:
        super().__init__(
            className="fade-in-right",
            id=self.ids.card(user_data.id),
            children=dmc.Group(
                [
                    dmc.Avatar(get_initials(user_data.name), radius="xl"),
                    dmc.Stack(
                        [
                            dmc.Text(
                                user_data.name,
                                fw="bold",
                                fz="md",
                                style={
                                    "overflow": "hidden",
                                    "textOverflow": "ellipsis",
                                    "whiteSpace": "nowrap"
                                }
                            ),
                            dmc.Text(
                                user_data.email,
                                fz="sm",
                                c="gray",
                                style={
                                    "overflow": "hidden",
                                    "textOverflow": "ellipsis",
                                    "whiteSpace": "nowrap"
                                }
                            ),
                        ],
                        gap=0,
                        style={"minWidth": 0, "flex": 1}
                    ),
                    dmc.Button(
                        "Delete",
                        id=self.ids.delete_btn(user_data.id),
                        color="red",
                        variant="light",
                        size="xs",
                        ml="auto",
                        **{"data-user-name": user_data.name}
                    ),
                    dmc.Button(
                        "Edit",
                        id=self.ids.edit_btn(user_data.id),
                        color="blue",
                        variant="light",
                        size="xs",
                        **{"data-user-name": user_data.name, "data-user-email": user_data.email}
                    ),
                ],
                wrap="nowrap",
            )
        )


@callback(
    *UserForm.callback_inputs,
    running=[(Output(UserForm.ids.submit_button, "loading"), True, False)],
    prevent_initial_call=True,
)
async def store_user(
    _,
    edit_data: Dict[str, int],
    name: str,
    email: str
):
    try:
        User(name=name, email=email)
    except ValidationError as e:
        errors_dict = parse_validation_errors(e, User)
        UserForm.set_error_state(
            name_error=errors_dict.get("name"),
            email_error=errors_dict.get("email")
        )
        return
    except Exception as e:
        # Handle any other unexpected errors
        NotificationsContainer.send_notification(
            title="Error",
            message=str(e),
            color="red",
        )
        return

    await asyncio.sleep(1)

    if edit_data:
        edit_id = edit_data["user_id"]
        edit_index = edit_data["index"]
        updated = update_user(edit_id, name, email)
        if not updated:
            NotificationsContainer.send_notification(
                title="Error",
                message=f"Information for user {name} could not be updated.",
            )
            return

        UserCard.update(updated, edit_index)
        NotificationsContainer.send_notification(
            title="Success",
            message=f"{updated.name} information has been successfully updated.",
            color="green",
        )

    else:
        user = add_user_to_json(name, email)
        card = UserCard(user)
        FeedComponent.add_child(card, prepend=True)

    UserModal.close()


@callback(Input(UserModal.ids.open_button, "n_clicks"))
def open_user_modal(_):
    form = UserForm()
    UserModal.open(form, "User Management")


@callback(Input(UserModal.ids.modal, "opened"))
def on_modal_opened(opened: bool):
    if not opened:
        UserModal.reset()

@callback(
    Input(UserCard.ids.delete_btn(ALL), "n_clicks"),
    State(UserCard.ids.delete_btn(ALL), "data-user-name"),
)
def init_delete(_, user_names: List[str]):
    triggered_id = ctx.triggered_id or {}
    user_id = triggered_id["user_id"]
    inputs = [x["id"] for x in ctx.inputs_list[-1]]
    idx = inputs.index(triggered_id)
    form = DeleteForm(user_name=user_names[idx], user_id=user_id, index=idx)
    UserModal.open(form, "Confirm Deletion")


@callback(
    Input(DeleteForm.ids.confirm_button, "n_clicks"),
    State(DeleteForm.ids.confirm_button, DeleteForm.ids.button_data),
    running=[(Output(DeleteForm.ids.confirm_button, "loading"), True, False)],
)
async def delete_user(_, user_data: Dict[str, int]):
    await asyncio.sleep(1)
    user_id = user_data["user_id"]
    idx = user_data["index"]
    deleted_user = delete_user_from_json(user_id)
    if not deleted_user:
        NotificationsContainer.send_notification(
            title="Error", message="User could not be deleted.", color="red"
        )
        return

    FeedComponent.remove_child(idx)
    UserModal.close()
    NotificationsContainer.send_notification(
        title="User Deleted",
        message=f"{deleted_user.name} has been successfully deleted.",
    )


@callback(
    Input(DeleteForm.ids.name_input, "value"),
    State(DeleteForm.ids.name_input, "placeholder"),
)
def validate_delete(name_input: str, user_name: str):
    if not user_name:
        return

    is_match = name_input.strip().lower() == user_name.strip().lower()
    DeleteForm.set_button_disabled(not is_match)


@callback(
    Input(UserCard.ids.edit_btn(ALL), "n_clicks"),
    State(UserCard.ids.edit_btn(ALL), "data-user-name"),
    State(UserCard.ids.edit_btn(ALL), "data-user-email"),
)
def init_edit_user(_, user_names: List[str], user_emails: List[str]):
    triggered_id = ctx.triggered_id or {}
    user_id = triggered_id["user_id"]
    inputs = [x["id"] for x in ctx.inputs_list[0]]
    idx = inputs.index(triggered_id)

    edit_data = {"user_id": user_id, "index": idx}
    form = UserForm(name=user_names[idx], email=user_emails[idx], edit_data=edit_data)
    UserModal.open(form, "Edit User")


@event_callback(
    Input(FeedComponent.ids.container, "id"),
    prevent_initial_call=False,
)
async def load_feed(_):
    await asyncio.sleep(1)
    yield stream_props([
        (FeedComponent.ids.container, {"children": []}),
        (UserModal.ids.open_button, {"disabled": False}),
    ])
    users = load_users()
    for user in users:
        await asyncio.sleep(0.2)
        user_card = UserCard(user)
        yield FeedComponent.add_child(user_card, stream=True)
