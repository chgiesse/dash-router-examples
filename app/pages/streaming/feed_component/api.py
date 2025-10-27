from pathlib import Path
from typing import Dict, Any, List
from pydantic import BaseModel, Field
import json

# Get the absolute path to the users.json file
USERS_FILE = Path(__file__).parent.parent.parent.parent / "assets" / "data" / "users.json"


class User(BaseModel):
    id: int | None = None
    name: str = Field(min_length=5, max_length=50)
    email: str = Field(pattern=r"[^@]+@[^@]+\.[^@]+", min_length=5)


def _read_raw() -> Dict[str, Any]:
    with open(str(USERS_FILE), "r") as f:
        return json.load(f)


def _write_raw(data: Dict[str, Any]):
    with open(str(USERS_FILE), "w") as f:
        json.dump(data, f, indent=2)


def load_users() -> List[User]:
    """Return a list of User model instances from the JSON store."""
    raw = _read_raw()
    users = [User(**u) for u in raw.get("users", [])]
    return users


def save_users_raw(data: Dict[str, Any]):
    """Write the raw data structure (dict with keys 'users' and 'next_id')."""
    _write_raw(data)


def add_user_to_json(name: str, email: str) -> User:
    """Add a new user to the JSON file and return the created User model."""
    data = _read_raw()
    # compute a sensible next_id if missing
    next_id = data.get("next_id")
    if next_id is None:
        existing_ids = [u.get("id", 0) for u in data.get("users", [])]
        next_id = (max(existing_ids) + 1) if existing_ids else 1
    user = User(id=next_id, name=name, email=email)
    data.setdefault("users", []).append(user.dict())
    data["next_id"] = next_id + 1
    _write_raw(data)
    return user


def delete_user_from_json(user_id: int) -> User | None:
    data = _read_raw()
    users = data.get("users", [])
    deleted_user = None

    for u in users:
        if u.get("id") == user_id:
            deleted_user = User(**u)
            break

    if deleted_user:
        data["users"] = [u for u in users if u.get("id") != user_id]
        _write_raw(data)
        return deleted_user
    return None


def load_user_by_id(user_id: int) -> User | None:
    """Return a User model for the given id, or None if not found."""
    data = _read_raw()
    for u in data.get("users", []):
        if u.get("id") == user_id:
            return User(**u)
    return None


def update_user(user_id: int, name: str | None = None, email: str | None = None) -> User | None:
    """Update an existing user's name/email and return the updated User, or None if not found."""
    data = _read_raw()
    users = data.get("users", [])
    for idx, u in enumerate(users):
        if u.get("id") == user_id:
            updated = u.copy()
            if name is not None:
                updated["name"] = name
            if email is not None:
                updated["email"] = email
            users[idx] = updated
            data["users"] = users
            _write_raw(data)
            return User(**updated)
    return None
