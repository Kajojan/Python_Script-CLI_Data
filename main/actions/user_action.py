import pandas as pd
import json


class User:
    def __init__(self, db, user):
        self.dataBase = db
        self.users = self.dataBase.get_data()
        self.user = user[0]

    def print_children(self):
        children = self.user["children"]
        children_sorted = sorted(children, key=lambda x: x["name"])
        return children_sorted

    def find_similar_children_by_age(self):
        data = self.users
        result = []
        for user in data:
            if user != self.user:
                children = list(filter(lambda y: y["age"] == 6, user["children"]))
                if len(children) > 0:
                    helper = {
                        "firstname": user["firstname"],
                        "telephone_number": user["telephone_number"],
                        "children": user["children"],
                    }
                    result.append(helper)

        return result

    def find_similar_childre_by_age_SQL(self):
        children = self.user["children"]
        id = self.user["id"]
        data = []
        for kids in children:
            other = self.dataBase.get_other_children(kids["age"], id)
            result_dict = [
                {
                    "firstname": firstname,
                    "telephone_number": telephone_number,
                    "children": sorted(json.loads(children), key=lambda x: x["name"]),
                }
                for firstname, telephone_number, children in other
            ]
            data.append(result_dict)
        list = [obj for sublist in data for obj in sublist]
        df = pd.DataFrame(list)
        df_no_duplicates = df.drop_duplicates(subset="telephone_number")
        unique_data = df_no_duplicates.to_dict(orient="records")
        return unique_data
