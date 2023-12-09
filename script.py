import argparse
import os.path
import sys

from main.Login.Login import Login
from main.actions.action_manager import ActionManager
from main.db.db import DB


class Script:
    def __init__(self, db_path: str) -> None:
        self.db_path = db_path
        if os.path.exists(db_path):
            self.dataBase = DB()
            self.dataBase.connect(db_path)
            self.is_login = Login(self.dataBase)

    def main(self) -> None:
        parser = argparse.ArgumentParser()

        parser.add_argument("--login", help="Login użytkownika")
        parser.add_argument("--password", help="Hasło użytkownika")
        parser.add_argument(
            "command",
            choices=[
                "print-all-accounts",
                "print-oldest-account",
                "group-by-age",
                "print-children",
                "find-similar-children-by-age",
                "create_database",
            ],
            help="Wybierz komendę do wykonania",
        )
        args = parser.parse_args()
        command = args.command

        if command != "create_database":
            if args.login is None or args.password is None:
                parser.error(
                    "Wymagane są argumenty --login i --password dla tej komendy."
                )
        else:
            if os.path.exists(self.db_path):
                self.dataBase.remove(self.db_path)
            self.dataBase.create(self.db_path)
            print("creating database...")
            self.through_path("./main/db/data")
            sys.exit()

        login = args.login
        password = args.password

        data = self.is_login.is_login(password, login)
        if data["status"]:
            self.user = data["data"]
            self.action = ActionManager(self.dataBase, self.user)
            self.action_user = self.action.get_action(self.user[0]["role"])
            try:
                match command:
                    case "print-all-accounts":
                        print(self.action_user.prtint_all_accounts())
                    case "print-oldest-account":
                        for (
                            key,
                            value,
                        ) in self.action_user.print_oldest_account().items():
                            print(f"{key}: {value} ")
                    case "group-by-age":
                        data = self.action_user.group_by_age()
                        for group in data:
                            print("-----")
                            for key, value in group.items():
                                print(f"{key}: {value} ")
                    case "print-children":
                        data = self.action_user.print_children()
                        for object in data:
                            print("-----")
                            for key, value in object.items():
                                print(f"{key}: {value} ")

                    case "find-similar-children-by-age":
                        data = self.action_user.find_similar_childre_by_age_SQL()
                        for kids in data:
                            print("-----")
                            res = ""
                            res += f'{kids["firstname"]}, {kids["telephone_number"]}:  '
                            for child in kids["children"]:
                                res += f'{child["name"]}, {child["age"]}; '

                            print(res)
            except:
                print(
                    "permission denied:  you are allow to use  print-children or find-similar-children-by-age "
                )
        else:
            print(f"Valid Login- {data['message']}")

    def through_path(self, path):
        try:
            for element in os.listdir(path):
                full_path = os.path.join(path, element)

                if os.path.isfile(full_path):
                    print(f"loading file: {element}")
                    self.dataBase.loda_data_and_add(full_path)
                elif os.path.isdir(full_path):
                    self.through_path(full_path)

        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    script = Script("./db.sqlite3")
    script.main()
