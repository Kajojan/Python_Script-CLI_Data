import datetime
import sqlite3
import json

from sqlalchemy import Null
from main.db.data_loader import *
import bcrypt


class DB_manager:
    def __init__(self):
        self.conn = None
        self.cursor = None

    def connect(self, db_path: str):
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()

    def create_db(self, db_path: str):
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.cursor = self.conn.cursor()
        create_table_query = """
            CREATE TABLE IF NOT EXISTS Users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            firstname TEXT,
            telephone_number TEXT,
            email TEXT,
            password TEXT,
            role TEXT,
            created_at DATETIME,
            parent_id INTEGER,
            FOREIGN KEY (parent_id) REFERENCES Users(id)
        );"""
        create_children_table_query = """
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

    def add_to_database(self, data):
        for user_data in data:
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
            user_id = self.cursor.lastrowid
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

    def get_data_from_database(self):
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
        data = self.cursor.fetchall()
        results = self.to_json(data)

        return results


    def remove_from_database(self, id):
        self.cursor.execute("DELETE FROM Users WHERE id = ?", (id,))
        self.cursor.execute("DELETE FROM Children WHERE user_id = ?", (id,))
        self.conn.commit()

    def get_from_databse_by_id(self, id):
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
        results = self.to_json(self.cursor.fetchall())

        return results

    def get_from_databse_by_number(self, number):
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

        data = self.cursor.fetchone()
        results = None
        if data != None:
            results = self.to_json([data])

        return results

    def get_from_databse_by_email(self, email):
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
        data = self.cursor.fetchone()
        results = None
        if data != None:
            results = self.to_json([data])

        return results

    def closeDb(self):
        self.conn.close()

    def hash_password(self, password):
        return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

    def is_hash_password(self, password, hash_password):
        return bcrypt.checkpw(password.encode("utf-8"), hash_password)

    def get_password(self, email_number):
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

        data = self.cursor.fetchone()
        if data != None:
            return data[0]

        return None

    def drop_db(self):
        self.cursor.execute("DROP TABLE IF EXISTS Users;")
        self.cursor.execute("DROP TABLE IF EXISTS Children;")
        self.conn.commit()
        self.conn.close()

    def remove(self, path):
        try:
            os.remove(path)
        except FileNotFoundError:
            raise FileNotFoundError
        except Exception as e:
            raise e

    def to_json(self, data):
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
