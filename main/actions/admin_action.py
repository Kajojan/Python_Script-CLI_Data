from typing import Any

import pandas as pd
from pandas import DataFrame

from main.actions.user_action import User_action
from main.db.db import DB


class Admin_action(User_action):
    def __init__(self, db: DB, user: list) -> None:
        super().__init__(db, user)

    def prtint_all_accounts(self) -> int:
        number_of_account: int = len(self.users)
        return number_of_account

    def print_oldest_account(self) -> dict:
        data: list[dict] = self.users
        oldest: list[dict] = sorted(data, key=lambda user: user["created_at"])
        return oldest[0]

    def group_by_age(self) -> dict:
        data: list[dict] = self.users
        children = list(map(lambda x: x["children"], data))
        children = [item for row in children for item in row]
        children.sort(key=lambda x: x["age"])
        df: DataFrame = pd.DataFrame(children)
        grouped_children: Any = (
            df.groupby("age")
            .size()
            .reset_index(name="count")
            .sort_values(["count"], ascending=True)
        )

        result: dict = grouped_children.to_dict(orient="records")
        return result
