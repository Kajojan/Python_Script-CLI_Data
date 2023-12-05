from main.db.data_loader import data_loader
from main.db.db_manager import DB_manager
import sqlite3


class DB:
    def __init__(self) -> None:
        self.dataBase = DB_manager()
        self.load_manager = data_loader()

    def create(self, db_path):
        self.dataBase.create_db(db_path)

    def connect(self, db_path):
        self.dataBase.connect(db_path)

    def remove(self, db_path):
        self.dataBase.remove(db_path)

    def loda_data_and_add(self, path):
        data = self.load_manager.file_load(path)
        valid_data = self.load_manager.validation(data)
        self.dataBase.add_to_database(valid_data)

    def get_data_by_telefone_number(self, number):
        return self.dataBase.get_from_databse_by_number(number)

    def get_password(self, email_number):
        return self.dataBase.get_password(email_number)

    def get_data_by_email(self, email):
        return self.dataBase.get_from_databse_by_email(email)

    def get_data_by_id(self, user_id):
        return self.dataBase.get_from_databse_by_id(user_id)

    def get_data(self):
        return self.dataBase.get_data_from_database()

    def delete_data_by_id(self, user_id):
        return self.dataBase.remove_from_database(user_id)

    def drop_db(self):
        self.dataBase.drop_db()

    def close_db(self):
        self.dataBase.closeDb()
