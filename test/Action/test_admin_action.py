import unittest
from main.db.db import DB
from main.actions.admin_action import Admin_action


class TestAdmin(unittest.TestCase):
    def setUp(self) -> None:
        self.database: DB = DB()
        self.database.remove("./test/db.sqlite3")
        self.database.create("./test/db.sqlite3")
        self.database.loda_data_and_add("./test/Action/test_csv_action.csv")
        self.action: Admin_action = Admin_action(
            self.database, self.database.get_data_by_telefone_number("612660796")
        )

    def test_print_all_accounts(self):
        result: int = self.action.prtint_all_accounts()
        expected_result: int = 2
        self.assertEqual(result, expected_result)

    def test_print_oldest_account(self):
        result: dict = self.action.print_oldest_account()
        expected_result = {
            "name": "Don",
            "email_address": "tamara@example.com",
            "created_at": "2023-07-23 23:27:09",
        }

        self.assertEqual(result, expected_result)

    def test_group_by_age(self):
        result: dict = self.action.group_by_age()
        expected_result = [
            {"age": 1, "count": 2},
            {"age": 6, "count": 2},
            {"age": 12, "count": 2},
        ]
        self.assertEqual(result, expected_result)


if __name__ == "__main__":
    unittest.main()
