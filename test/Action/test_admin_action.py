import unittest
from main.db.db import DB
from main.Login.Login import Login
from main.actions.admin_action import Admin


class TestMyModule(unittest.TestCase):
    def setUp(self) -> None:
        self.database = DB()
        self.database.remove("./test/db.sqlite3")
        self.database.create("./test/db.sqlite3")
        self.database.loda_data_and_add("./test/Action/test_csv_action.csv")
        self.action = Admin(self.database)

    def test_print_all_accounts(self):
        result = self.action.prtint_all_accounts()
        expected_result = 2
        self.assertEqual(result, expected_result)

    def test_print_oldest_account(self):
        result = self.action.print_oldest_account()
        expected_result = {
            "id": 2,
            "firstname": "Don",
            "telephone_number": "123456789",
            "email": "tamara@example.com",
            "role": "admin",
            "created_at": "2023-07-23 23:27:09",
            "children": [
                {"name": "Judith", "age": 1},
                {"name": "Michael", "age": 12},
                {"name": "Theresa", "age": 6},
            ],
        }

        self.assertEqual(result, expected_result)

    def test_group_by_age(self):
        result = self.action.group_by_age()
        expected_result = [
            {"age": 1, "count": 2},
            {"age": 6, "count": 2},
            {"age": 12, "count": 2},
        ]
        self.assertEqual(result, expected_result)



if __name__ == "__main__":
    unittest.main()
