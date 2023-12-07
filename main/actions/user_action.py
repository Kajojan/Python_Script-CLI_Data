import pandas as pd
import json

from pandas import DataFrame

from main.db.db import DB


class User_action:
    def __init__(self, db: DB, user: list):
        self.dataBase: DB = db
        self.users: list[dict] = self.dataBase.get_data()
        self.user: dict = user[0]

    def print_children(self) -> list[dict]:
        children: list[dict] = self.user["children"]
        children_sorted: list[dict] = sorted(children, key=lambda x: x["name"])
        return children_sorted

    def find_similar_children_by_age(self) -> list[dict]:
        data: list[dict] = self.users
        result: list[dict] = []
        for user in data:
            if user != self.user:
                children: list = list(filter(lambda y: y["age"] == 6, user["children"]))
                if len(children) > 0:
                    helper: dict = {
                        "firstname": user["firstname"],
                        "telephone_number": user["telephone_number"],
                        "children": user["children"],
                    }
                    result.append(helper)

        return result

    def find_similar_childre_by_age_SQL(self) -> list[dict]:
        children: list[dict] = self.user["children"]
        id: int = self.user["id"]
        data: list[list[dict]] = []
        for kids in children:
            other: list = self.dataBase.get_other_children(kids["age"], id)
            result_dict: list[dict] = [
                {
                    "firstname": firstname,
                    "telephone_number": telephone_number,
                    "children": sorted(json.loads(children), key=lambda x: x["name"]),
                }
                for firstname, telephone_number, children in other
            ]
            data.append(result_dict)
        list_flatten: list[dict] = [obj for sublist in data for obj in sublist]
        df: DataFrame = pd.DataFrame(list_flatten)
        df_no_duplicates: DataFrame = df.drop_duplicates(subset="telephone_number")
        unique_data: list[dict] = df_no_duplicates.to_dict(orient="records")
        return unique_data
