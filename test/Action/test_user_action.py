import unittest
from main.db.db import DB
from main.actions.user_action import User


class TestMyModule(unittest.TestCase):
    def setUp(self) -> None:
        self.database: DB = DB()
        self.database.remove("./test/db.sqlite3")
        self.database.create("./test/db.sqlite3")
        self.database.loda_data_and_add("./test/Action/test_csv_action.csv")
        user: list[dict] = self.database.get_data_by_telefone_number("612660796")
        self.action: User = User(self.database, user)

    def test_print_children(self):
        result: list[dict] = self.action.print_children()
        expected_result = [
            {"name": "Judith", "age": 1},
            {"name": "Michael", "age": 12},
            {"name": "Theresa", "age": 6},
        ]
        self.assertEqual(result, expected_result)

    def test_find_similar_children_by_age(self):
        result: list[dict] = self.action.find_similar_children_by_age()
        expected_result = [
            {
                "firstname": "Don",
                "telephone_number": "123456789",
                "children": [
                    {"name": "Judith", "age": 1},
                    {"name": "Michael", "age": 12},
                    {"name": "Theresa", "age": 6},
                ],
            }
        ]

        self.assertEqual(result, expected_result)

    def test_find_similar_children_by_age_SQL(self):
        result: list[dict] = self.action.find_similar_childre_by_age_SQL()
        expected_result = [
            {
                "firstname": "Don",
                "telephone_number": "123456789",
                "children": [
                    {"name": "Judith", "age": 1},
                    {"name": "Michael", "age": 12},
                    {"name": "Theresa", "age": 6},
                ],
            }
        ]

        self.assertEqual(result, expected_result)


if __name__ == "__main__":
    unittest.main()
