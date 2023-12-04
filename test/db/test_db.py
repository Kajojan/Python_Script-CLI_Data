import unittest
import os
import sys
sys.path.append('../../')

from main.db.data_loader import data_loader
from main.db.db_manager import DB_manager


class TestMyModule(unittest.TestCase):
    def setUp(self):
        self.loader_manager = data_loader()

    def test_load_file_not_found(self):
        with self.assertRaises("FileNotFound"):
            self.loader_manager.file_load("file")

    def test_load_files(self):
        result_csv = self.loader_manager.file_load("./fake_data/test_file.csv")
        result_json = self.loader_manager.file_load("./fake_data/test_file.json")
        result_mxl = self.loader_manager.file_load("./fake_data/test_file.mxl")

        expected_result = [{"Name": "John", "Age": 30}]

        self.assertEqual(result_csv, expected_result)
        self.assertEqual(result_json, expected_result)
        self.assertEqual(result_mxl, expected_result)

    def test_validation_number(self):
        result_csv = self.loader_manager.number(
            self.loader_manager.file_load("./fake_data/test_file_validation.csv")
        )
        result = [
            {
                "firstname": "John",
                "telephone_number": "123456789",
                "email": "alice@example.com",
            },
            {
                "firstname": "Alice",
                "telephone_number": "123456789",
                "email": "@example.com",
            },
            {
                "firstname": "Eva",
                "telephone_number": "+48213456789",
                "email": "john@.com",
            },
            {
                "firstname": "John",
                "telephone_number": "00132456789",
                "email": "eva@example.com",
            },
            {
                "firstname": "Eva",
                "telephone_number": "555-123-457",
                "email": "michael@example.",
            },
            {
                "firstname": "Michael",
                "telephone_number": "(48) 124356789",
                "email": "david@example.com",
            },
            {
                "firstname": "David",
                "telephone_number": "123 465 789",
                "email": "david@example.com",
            },
        ]

        self.assertEqual(result_csv, result)

    def test_validation_email(self):
        result_csv = self.loader_manager.email(
            self.loader_manager.file_load("./fake_data/test_file_validation.csv")
        )
        result = [
            {
                "firstname": "David",
                "telephone_number": "123 465 789",
                "email": "david@example.com",
            },
            {
                "firstname": "David2",
                "telephone_number": "123 4659 789",
                "email": "david2@example.com",
            },
        ]
        self.assertEqual(result_csv, result)

    def test_validation(self):
        result_csv = self.loader_manager.validation(
            self.loader_manager.file_load("./fake_data/test_file_validation.csv")
        )
        result = [
            {
                "firstname": "David",
                "telephone_number": "123465789",
                "email": "david@example.com",
            },
        ]
        self.assertEqual(result_csv, result)

    def test_create_db(self):
        db_path = "./db.sqlite3"
        dataBase = DB_manager()
        dataBase.create_db(db_path)

        self.assertTrue(os.path.exists(db_path))
        os.remove(db_path)
        self.assertFalse(os.path.exists(db_path))

    def test_add_receive_delete_from_db(self):
        db_path = "./db.sqlite3"
        dataBase = DB_manager()
        dataBase.create_db(db_path)

        data = {"name": "John", "age": 30}
        dataBase.add_to_database(data)
        retrieved_data = dataBase.get_data_from_database()

        self.assertEqual(data, retrieved_data)

        dataBase.remove_from_database(data)
        retrieved_data = dataBase.get_data_from_database()
        expectedData = []

        self.assertEqual(expectedData, retrieved_data)


if __name__ == "__main__":
    unittest.main()
