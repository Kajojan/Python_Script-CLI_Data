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

    def create_db(self, db_path: str):
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.cursor = self.conn.cursor()
        create_table_query: str = """
            CREATE TABLE IF NOT EXISTS Users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            firstname TEXT,
            telephone_number TEXT UNIQUE,
            email TEXT UNIQUE,
            password TEXT,
            role TEXT,
            created_at DATETIME,
            parent_id INTEGER,
            FOREIGN KEY (parent_id) REFERENCES Users(id)
        );"""
        create_children_table_query: str = """
        CREATE TABLE IF NOT EXISTS Children (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            name TEXT,
            age INTEGER,
            FOREIGN KEY (user_id) REFERENCES Users(id)
        );
                """
        self.cursor.execute(create_table_query)
        self.cursor.execute(create_children_table_query)

        self.conn.commit()

    def add_to_database(self, data: list[dict]):
        for user_data in data:
            try:
                self.cursor.execute(
                    """
                INSERT INTO Users (firstname, telephone_number, email, password, role, created_at)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
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
                            """
                            INSERT INTO Children (user_id, name, age)
                            VALUES (?, ?, ?)
                        """,
                            (user_id, child["name"], child["age"]),
                        )

                self.conn.commit()
            except:
                # i think timestamp is a created_at value if not we could delete lines from 81 to 83, then you would add new account based on loading file

                other_user = self.get_from_databse_by_number(
                    user_data["telephone_number"]
                )[0]
                date_time1 = datetime.strptime(
                    other_user["created_at"], "%Y-%m-%d %H:%M:%S"
                )
                date_time2 = datetime.strptime(
                    user_data["created_at"], "%Y-%m-%d %H:%M:%S"
                )
                if date_time1 > date_time2:
                    self.remove_from_database(other_user["id"])
                    self.cursor.execute(
                        """
                    INSERT INTO Users (firstname, telephone_number, email, password, role, created_at)
                    VALUES (?, ?, ?, ?, ?, ?)
                    """,
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
                    if "children" in user_data and isinstance(
                        user_data["children"], list
                    ):
                        for child in user_data["children"]:
                            self.cursor.execute(
                                """
                                INSERT INTO Children (user_id, name, age)
                                VALUES (?, ?, ?)
                            """,
                                (user_id, child["name"], child["age"]),
                            )

                    self.conn.commit()

    def get_data_from_database(self) -> list[dict]:
        self.cursor.execute(
            """
            SELECT Users.id, Users.firstname, Users.telephone_number, Users.email, Users.role, Users.created_at,
            json_group_array( json_object('name', Children.name, 'age', Children.age)) AS children
            FROM Users 
            LEFT JOIN
            Children ON Users.id = Children.user_id
            GROUP BY Users.id;
        """
        )
        data: list = self.cursor.fetchall()
        results: list[dict] = self.to_json(data)

        return results

    def get_other_children(self, age: int, user_id: int) -> list:
        self.cursor.execute(
            """
            SELECT Users.firstname, Users.telephone_number,
            json_group_array( json_object('name', Children.name, 'age', Children.age)) AS children
            FROM Users
            JOIN Children  ON Users.id = Children.user_id
            WHERE Users.id IN (
                SELECT DISTINCT user_id
                FROM Children
                WHERE age = ? )   
            AND Users.id != ?
            GROUP BY Users.id;
        """,
            (
                age,
                user_id,
            ),
        )
        data: list = self.cursor.fetchall()

        return data

    def remove_from_database(self, id: int) -> None:
        self.cursor.execute("DELETE FROM Users WHERE id = ?", (id,))
        self.cursor.execute("DELETE FROM Children WHERE user_id = ?", (id,))
        self.conn.commit()

    def get_from_databse_by_id(self, id: int) -> list[dict]:
        self.cursor.execute(
            """
            SELECT Users.id, Users.firstname, Users.telephone_number, Users.email, Users.role, Users.created_at,
            json_group_array( json_object('name', Children.name, 'age', Children.age)) AS children
            FROM Users 
            LEFT JOIN
            Children ON Users.id = Children.user_id
            WHERE Users.id = ?
            GROUP BY Users.id;
        """,
            (id,),
        )
        results: list[dict[str, list[Any] | Any]] = self.to_json(self.cursor.fetchall())

        return results

    def get_from_databse_by_number(self, number: str) -> list[dict]:
        self.cursor.execute(
            """
            SELECT Users.id, Users.firstname, Users.telephone_number, Users.email, Users.role, Users.created_at,
            json_group_array( json_object('name', Children.name, 'age', Children.age)) AS children
            FROM Users 
            LEFT JOIN
            Children ON Users.id = Children.user_id
            WHERE Users.telephone_number = ?
            GROUP BY Users.id;
        """,
            (number,),
        )

        data: object = self.cursor.fetchone()
        results = None
        if data is not None:
            results = self.to_json([data])

        return results

    def get_from_databse_by_email(self, email: str) -> List[dict]:
        self.cursor.execute(
            """
            SELECT Users.id, Users.firstname, Users.telephone_number, Users.email, Users.role, Users.created_at,
            json_group_array( json_object('name', Children.name, 'age', Children.age)) AS children
            FROM Users 
            LEFT JOIN
            Children ON Users.id = Children.user_id
            WHERE Users.email = ?
            GROUP BY Users.id;
        """,
            (email,),
        )
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
