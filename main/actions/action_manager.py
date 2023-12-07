from typing import Any

from main.actions.admin_action import Admin_action
from main.actions.user_action import User_action
from main.db.db import DB


class ActionManager:
    def __init__(self, db: DB, user: list) -> None:
        self.actions: dict = {
            "admin": Admin_action(db, user),
            "user": User_action(db, user),
        }

    def get_action(self, value: str) -> Any:
        if value in self.actions:
            return self.actions[value]
        raise FileNotFoundError(f"Action not found")

    def add_action(self, name: str, action: object) -> None:
        self.actions[name] = action

    def delete_action(self, name: str) -> None:
        del self.actions[name]
