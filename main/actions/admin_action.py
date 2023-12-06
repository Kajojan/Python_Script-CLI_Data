import pandas as pd
import json

from sympy import true


class Admin:
    def __init__(self, db):
        self.dataBase = db
        self.users = self.dataBase.get_data()

    def prtint_all_accounts(self):
        number_of_account = len(self.users)
        return number_of_account

    def print_oldest_account(self):
        data = self.users
        oldest = sorted(data, key=lambda user: user["created_at"])
        return oldest[0]

    def group_by_age(self):
        data = self.users
        children = list(map(lambda x: x["children"], data))
        children = [item for row in children for item in row]
        children.sort(key=lambda x: x["age"])
        df = pd.DataFrame(children)
        grouped_children = (
            df.groupby("age")
            .size()
            .reset_index(name="count")
            .sort_values(["count"], ascending=True)
        )

        result = grouped_children.to_dict(orient="records")
        return result
