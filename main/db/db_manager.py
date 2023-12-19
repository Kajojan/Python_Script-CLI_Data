import sqlite3
import json
import os
from datetime import datetime
from typing import List, Any

import bcrypt


class DB_manager:
    def __init__(self) -> None:
        self.conn = None
        self.cursor = None

    def connect(self, db_path: str) -> None:
        self.conn: sqlite3.Connection = sqlite3.connect(db_path)
        self.cursor: sqlite3.Cursor = self.conn.cursor()

    def read_sql_file(self, file_path: str):
        with open(file_path, "r") as file:
            return file.read()

    def create_db(self, db_path: str):
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.cursor = self.conn.cursor()
        create_table_query = self.read_sql_file("main/db/SQL/create_table.sql")
        self.cursor.execute(create_table_query)
        create_children_table_query = self.read_sql_file(
            "main/db/SQL/create_table_children.sql"
        )
        self.cursor.execute(create_children_table_query)
        self.conn.commit()

    def add_to_database(self, data: list[dict]):
        insert_user_query = self.read_sql_file("main/db/SQL/insert_user.sql")
        insert_child_query = self.read_sql_file("main/db/SQL/insert_child.sql")

        for user_data in data:
            try:
                self.cursor.execute(
                    insert_user_query,
                    (
                        user_data["firstname"],
                        user_data["telephone_number"],
                        user_data["email"],
                        self.hash_password(user_data["password"]),
                        user_data["role"],
                        user_data["created_at"],
                    ),
                )
                user_id: object = self.cursor.lastrowid
                if "children" in user_data and isinstance(user_data["children"], list):
                    for child in user_data["children"]:
                        self.cursor.execute(
                            insert_child_query,
                            (user_id, child["name"], child["age"]),
                        )

                self.conn.commit()
            except:
                # if we think  timestamp is a created_at value we could should uncomment  lines from 69 to 75, then you would add new account based on created_at

                other_user = self.get_from_databse_by_number(
                    user_data["telephone_number"]
                )
                if other_user is None:
                    other_user = self.get_from_databse_by_email(user_data["email"])
                other_user = other_user[0]
                # date_time1 = datetime.strptime(
                #     other_user["created_at"], "%Y-%m-%d %H:%M:%S"
                # )
                # date_time2 = datetime.strptime(
                #     user_data["created_at"], "%Y-%m-%d %H:%M:%S"
                # )
                # if date_time1 > date_time2:
                self.remove_from_database(other_user["id"])
                self.cursor.execute(
                    insert_user_query,
                    (
                        user_data["firstname"],
                        user_data["telephone_number"],
                        user_data["email"],
                        self.hash_password(user_data["password"]),
                        user_data["role"],
                        user_data["created_at"],
                    ),
                )
                user_id: object = self.cursor.lastrowid

                if "children" in user_data and isinstance(user_data["children"], list):
                    for child in user_data["children"]:
                        self.cursor.execute(
                            insert_child_query,
                            (user_id, child["name"], child["age"]),
                        )

                self.conn.commit()

    def get_data_from_database(self) -> list[dict]:
        select_query = self.read_sql_file("main/db/SQL/get_data_from_db.sql")
        self.cursor.execute(select_query)
        data: list = self.cursor.fetchall()
        results: list[dict] = self.to_json(data)

        return results

    def get_other_children(self, age: int, user_id: int) -> list:
        select_query = self.read_sql_file("main/db/SQL/get_other_children.sql")
        self.cursor.execute(select_query, (age, user_id))
        data: list = self.cursor.fetchall()

        return data

    def remove_from_database(self, id: int) -> None:
        self.cursor.execute("DELETE FROM Users WHERE id = ?", (id,))
        self.cursor.execute("DELETE FROM Children WHERE user_id = ?", (id,))
        self.conn.commit()

    def get_from_databse_by_id(self, id: int) -> list[dict]:
        select_query = self.read_sql_file("main/db/SQL/get_by_id.sql")
        self.cursor.execute(select_query, (id,))
        results: list[dict[str, list[Any] | Any]] = self.to_json(self.cursor.fetchall())

        return results

    def get_from_databse_by_number(self, number: str) -> list[dict]:
        select_query = self.read_sql_file("main/db/SQL/get_by_number.sql")
        self.cursor.execute(select_query, (number,))
        data: object = self.cursor.fetchone()
        results = None
        if data is not None:
            results = self.to_json([data])

        return results

    def get_from_databse_by_email(self, email: str) -> List[dict]:
        select_query = self.read_sql_file("main/db/SQL/get_by_email.sql")
        self.cursor.execute(select_query, (email,))
        data: object = self.cursor.fetchone()
        results = None
        if data is not None:
            results = self.to_json([data])

        return results

    def closeDb(self) -> None:
        self.conn.close()

    def hash_password(self, password: str) -> bytes:
        return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

    def is_hash_password(self, password: str, hash_password: bytes) -> bool:
        return bcrypt.checkpw(password.encode("utf-8"), hash_password)

    def get_password(self, email_number: str) -> bytes:
        if "@" in email_number:
            self.cursor.execute(
                """
                SELECT Users.password
                FROM Users 
                WHERE Users.email = ?
            """,
                (email_number,),
            )
        else:
            self.cursor.execute(
                """
                SELECT Users.password
                FROM Users 
                WHERE Users.telephone_number = ?
            """,
                (email_number,),
            )

        data: List = self.cursor.fetchone()
        if data is not None:
            return data[0]

        return None

    def drop_db(self) -> None:
        self.cursor.execute("DROP TABLE IF EXISTS Users;")
        self.cursor.execute("DROP TABLE IF EXISTS Children;")
        self.conn.commit()
        self.conn.close()

    def remove(self, path: str) -> None:
        try:
            os.remove(path)
        except FileNotFoundError:
            raise FileNotFoundError
        except Exception as e:
            raise e

    def to_json(self, data: list) -> List[dict]:
        user_list = []
        for row in data:
            (
                user_id,
                firstname,
                telephone_number,
                email,
                role,
                created_at,
                children_json_str,
            ) = row

            user_dict = {
                "id": user_id,
                "firstname": firstname,
                "telephone_number": telephone_number,
                "email": email,
                "role": role,
                "created_at": created_at,
                "children": [],
            }

            if children_json_str != '[{"name":null,"age":null}]':
                children_list = json.loads(children_json_str)
                user_dict["children"] = children_list
            user_list.append(user_dict)

        return user_list
