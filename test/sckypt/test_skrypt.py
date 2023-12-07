import unittest
from main.db.db import DB
from main.Login.Login import Login


class TestMyModule(unittest.TestCase):
    def setUp(self):
        self.database: DB = DB()
        self.database.create("./test/db.sqlite3")
        self.database.loda_data_and_add("./test/login/test_csv_login.csv")
        self.login: Login = Login(self.database)


if __name__ == "__main__":
    unittest.main()
