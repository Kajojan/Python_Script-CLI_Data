from main.db.data_loader import data_loader
from main.db.db_manager import DB_manager


class DB:
    def __init__(self) -> None:
        self.dataBase: DB_manager = DB_manager()
        self.load_manager: data_loader = data_loader()

    def create(self, db_path: str) -> None:
        self.dataBase.create_db(db_path)

    def connect(self, db_path: str) -> None:
        self.dataBase.connect(db_path)

    def remove(self, db_path: str) -> None:
        self.dataBase.remove(db_path)

    def loda_data_and_add(self, path: str) -> None:
        data: list[dict] = self.load_manager.file_load(path)
        valid_data: list[dict] = self.load_manager.validation(data)
        self.dataBase.add_to_database(valid_data)

    def get_data_by_telefone_number(self, number: str) -> list[dict]:
        return self.dataBase.get_from_databse_by_number(number)

    def get_password(self, email_number: str) -> bytes:
        return self.dataBase.get_password(email_number)

    def get_data_by_email(self, email: str) -> list[dict]:
        return self.dataBase.get_from_databse_by_email(email)

    def get_data_by_id(self, user_id: int) -> list[dict]:
        return self.dataBase.get_from_databse_by_id(user_id)

    def get_data(self) -> list[dict]:
        return self.dataBase.get_data_from_database()

    def delete_data_by_id(self, user_id: int) -> None:
        return self.dataBase.remove_from_database(user_id)

    def get_other_children(self, age: int, user_id: int) -> list:
        return self.dataBase.get_other_children(age, user_id)

    def drop_db(self) -> None:
        self.dataBase.drop_db()

    def close_db(self) -> None:
        self.dataBase.closeDb()
