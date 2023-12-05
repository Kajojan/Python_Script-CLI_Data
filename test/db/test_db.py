import unittest
import os
import sys

sys.path.append("../../")

from main.db.data_loader import data_loader
from main.db.db_manager import DB_manager


class TestMyModule(unittest.TestCase):
    def setUp(self):
        self.loader_manager = data_loader()

    def test_load_file_not_found(self):
        with self.assertRaises(FileNotFoundError):
            self.loader_manager.file_load("file")

    def test_load_files_json(self):
        result_json = self.loader_manager.file_load("test/db/fake_data/test_file.json")

        expected_result = [
            {
                "firstname": "Justin",
                "telephone_number": "678762794",
                "email": "opoole@example.org",
                "password": "+3t)mSM6xX",
                "role": "admin",
                "created_at": "2022-11-25 02:19:37",
                "children": [],
            }
        ]
        self.assertEqual(result_json, expected_result)

    def test_load_files_csv(self):
        result_csv = self.loader_manager.file_load("test/db/fake_data/test_file.csv")
        expected_result = [
            {
                "firstname": "Don",
                "telephone_number": "612660796",
                "email": "tamara37@example.com",
                "password": "jQ66IIlR*1",
                "role": "user",
                "created_at": "2023-08-23 23:27:09",
                "children": [
                    {"name": "Michael", "age": 12},
                    {"name": "Theresa", "age": 6},
                    {"name": "Judith", "age": 1},
                ],
            }
        ]

        self.assertEqual(result_csv, expected_result)

    def test_load_files_xml(self):
        result_mxl = self.loader_manager.file_load("test/db/fake_data/test_file.xml")
        expected_result = [
            {
                "firstname": "Russell",
                "telephone_number": "+48817730653",
                "email": "jwilliams@example.com",
                "password": "4^8(Oj52C+",
                "role": "admin",
                "created_at": "2023-05-15 21:57:02",
                "children": None,
            }
        ]

        self.assertEqual(result_mxl, expected_result)

    def test_validation_number(self):
        result_csv = self.loader_manager.number(
            self.loader_manager.file_load("test/db/fake_data/test_file validation.csv")
        )
        result = [
            {
                "firstname": "Alice",
                "telephone_number": "123456789",
                "email": "@example.com",
            },
            {
                "firstname": "Alice",
                "telephone_number": "123456789",
                "email": "@example.com",
            },
            {"firstname": "Eva", "telephone_number": "213456789", "email": "john@.com"},
            {
                "firstname": "John",
                "telephone_number": "132456789",
                "email": "@eva@example.com",
            },
            {
                "firstname": "Eva",
                "telephone_number": "555123457",
                "email": "michael@example.",
            },
            {
                "firstname": "Michael",
                "telephone_number": "124356789",
                "email": "david@example.com",
            },
            {
                "firstname": "David",
                "telephone_number": "123465789",
                "email": "david@example.com",
            },
        ]

        self.assertEqual(result_csv, result)

    def test_validation_email(self):
        result_csv = self.loader_manager.email(
            self.loader_manager.file_load("test/db/fake_data/test_file validation.csv")
        )
        result = [
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
            {
                "firstname": "David2",
                "telephone_number": "123 4659 789",
                "email": "david2@example.com",
            },
        ]

        self.assertEqual(result_csv, result)

    def test_validation(self):
        result_csv = self.loader_manager.validation(
            self.loader_manager.file_load("test/db/fake_data/test_file validation.csv")
        )
        result = [
            {
                "firstname": "Michael",
                "telephone_number": "124356789",
                "email": "david@example.com",
            },
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
        dataBase.closeDb()

    def test_add_receive_delete_from_db(self):
        db_path = "./test/db.sqlite3"
        dataBase = DB_manager()
        dataBase.create_db(db_path)

        data = [
            {
                "firstname": "Justin",
                "telephone_number": "678762794",
                "email": "opoole@example.org",
                "password": "+3t)mSM6xX",
                "role": "admin",
                "created_at": "2022-11-25 02:19:37",
                "children": [{"name": "Anna", "age": 18}],
            },
            {
                "firstname": "Cathy",
                "telephone_number": "(48)594885352",
                "email": "rubengriffin@example.com",
                "password": "Dw2Bf(Dd!q",
                "role": "user",
                "created_at": "2023-08-27 16:39:04",
                "children": [],
            },
        ]
        dataBase.add_to_database(self.loader_manager.validation(data))
        retrieved_data = dataBase.get_data_from_database()
        data_expected = [
            {
                "id": 1,
                "firstname": "Justin",
                "telephone_number": "678762794",
                "email": "opoole@example.org",
                "role": "admin",
                "created_at": "2022-11-25 02:19:37",
                "children": [{"id": 1, "name": "Anna", "age": 18}],
            },
            {
                "id": 2,
                "firstname": "Cathy",
                "telephone_number": "594885352",
                "email": "rubengriffin@example.com",
                "role": "user",
                "created_at": "2023-08-27 16:39:04",
                "children": [],
            },
        ]
        self.assertEqual(data_expected, retrieved_data)

        dataBase.remove_from_database(1)
        dataBase.remove_from_database(2)

        retrieved_data = dataBase.get_data_from_database()
        expectedData = []

        self.assertEqual(expectedData, retrieved_data)
        dataBase.drop_db()
        dataBase.remove(db_path)

    def test_get_from_db_by_it(self):
        db_path = "./test/db.sqlite3"
        dataBase = DB_manager()
        dataBase.create_db(db_path)
        data = [
            {
                "firstname": "Justin",
                "telephone_number": "678762794",
                "email": "opoole@example.org",
                "password": "+3t)mSM6xX",
                "role": "admin",
                "created_at": "2022-11-25 02:19:37",
                "children": [{"name": "Anna", "age": 18}],
            }
        ]
        dataBase.add_to_database(self.loader_manager.validation(data))
        retrieved_data = dataBase.get_from_databse_by_id(1)
        data_expected = [
            {
                "id": 1,
                "firstname": "Justin",
                "telephone_number": "678762794",
                "email": "opoole@example.org",
                "role": "admin",
                "created_at": "2022-11-25 02:19:37",
                "children": [{"id": 1, "name": "Anna", "age": 18}],
            }
        ]

        email_data = dataBase.get_from_databse_by_email("opoole@example.org")
        telephone_data = dataBase.get_from_databse_by_number("678762794")

        dataBase.remove_from_database(1)

        dataBase.drop_db()
        dataBase.remove(db_path)

        self.assertEqual(retrieved_data, data_expected)
        self.assertEqual(email_data, data_expected)
        self.assertEqual(telephone_data, data_expected)

    def test_get_password(self):
        db_path = "./test/db.sqlite3"
        dataBase = DB_manager()
        dataBase.create_db(db_path)
        data = [
            {
                "firstname": "Justin",
                "telephone_number": "678762794",
                "email": "opoole@example.org",
                "password": "+3t)mSM6xX",
                "role": "admin",
                "created_at": "2022-11-25 02:19:37",
                "children": [{"name": "Anna", "age": 18}],
            }
        ]
        dataBase.add_to_database(self.loader_manager.validation(data))
        # get_by_number = dataBase.get_password("678762794")
        # get_by_emial = dataBase.get_password("opoole@example.org")
        get_None = dataBase.get_password('123')
        self.assertEqual(get_None, None)

        dataBase.drop_db()
        dataBase.remove(db_path)


if __name__ == "__main__":
    unittest.main()
