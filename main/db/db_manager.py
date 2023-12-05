import datetime
import sqlite3
from main.db.data_loader import *
import bcrypt


class DB_manager:
    def __init__(self):
        self.conn = None
        self.cursor = None

    def connect(self,db_path: str):
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

    def add_to_database(self, data: object):
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
                   Children.id AS child_id, Children.name AS child_name, Children.age AS child_age
            FROM Users
            LEFT JOIN Children ON Users.id = Children.user_id
        """
        )
        results = self.to_json(self.cursor.fetchall())

        return results

    def remove_from_database(self, id):
        self.cursor.execute("DELETE FROM Users WHERE id = ?", (id,))
        self.cursor.execute("DELETE FROM Children WHERE user_id = ?", (id,))
        self.conn.commit()

    def get_from_databse_by_id(self, id):
        self.cursor.execute(
            """
            SELECT Users.id, Users.firstname, Users.telephone_number, Users.email, Users.role, Users.created_at,
                   Children.id AS child_id, Children.name AS child_name, Children.age AS child_age
            FROM Users 
            LEFT JOIN Children ON Users.id = Children.user_id
            WHERE Users.id = ?
        """,
            (id,),
        )
        results = self.to_json(self.cursor.fetchall())

        return results

    def closeDb(self):
        self.conn.close()

    def hash_password(self, password):
        return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

    def is_hash_password(self, password, hash_password):
        return bcrypt.checkpw(password.encode("utf-8"), hash_password)

    def drop_db(self):
        self.cursor.execute("DROP TABLE IF EXISTS Users;")

        self.cursor.execute("DROP TABLE IF EXISTS Children;")
        self.conn.commit()
        self.conn.close()

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
                child_id,
                child_name,
                child_age,
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

            if child_id:
                user_dict["children"].append(
                    {"id": child_id, "name": child_name, "age": child_age}
                )

            user_list.append(user_dict)
        return user_list
