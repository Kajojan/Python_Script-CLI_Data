import unittest
from main.db.db import DB
from skrypt import Skrypt


class TestMyModule(unittest.TestCase):
    def setUp(self):
        self.database: DB = DB()
        self.database.create("./test/db.sqlite3")
        self.database.loda_data_and_add("./test/skrypt/test_csv_skrypt.csv")
        self.skrypt: Skrypt = Skrypt()
        self.skrypt.create_database()

    def test_successfull_login(self):
        number: str = "612660796"
        password: str = "jQ66IIlR*1"
        result: dict = self.skrypt.login(number, password)
        self.assertTrue(result["status"])


if __name__ == "__main__":
    unittest.main()
