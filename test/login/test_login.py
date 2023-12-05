import unittest
from main.db.db import DB
from main.Login.Login import Login


class TestMyModule(unittest.TestCase):
    def setUp(self):
        self.database = DB()
        self.database.create("./test/db.sqlite3")
        self.database.loda_data_and_add("./test/login/test_csv_login.csv")
        self.login = Login(self.database)

    def test_valid_phone(self):
        phone = "612660796"

        is_telephone_number = self.login.is_telephone_number(phone)

        self.assertTrue(is_telephone_number["status"])

    def test_not_valid_phone(self):
        phone_not_valid = "1234567899"
        is_telephone_number_not_valid = self.login.is_telephone_number(phone_not_valid)

        self.assertFalse(is_telephone_number_not_valid["status"])
        self.assertEqual(
            is_telephone_number_not_valid["message"], "Not Valid telephone number"
        )

    def test_not_found_phone(self):
        phone = "123456789"
        is_telephone_number = self.login.is_telephone_number(phone)
        self.assertFalse(is_telephone_number["status"])
        self.assertEqual(is_telephone_number["message"], "User Not Found")

    def test_valid_email(self):
        email = "tamara37@example.com"
        is_email = self.login.is_email(email)
        self.assertTrue(is_email["status"])

    def test_not_valid_emmail(self):
        email_not_valid = "@example.com"
        is_email_not_valid = self.login.is_email(email_not_valid)

        self.assertFalse(is_email_not_valid["status"])
        self.assertEqual(is_email_not_valid["message"], "Not Valid email")

    def test_not_found_email(self):
        email = "ta@example.com"
        is_email = self.login.is_email(email)
        self.assertFalse(is_email["status"])
        self.assertEqual(is_email["message"], "User Not Found")

    def test_login_correct(self):
        password_correct = "jQ66IIlR*1"
        email = "tamara37@example.com"
        result = self.login.is_login(password_correct, email)

        self.assertTrue(result["status"])

    def test_login_incorect_wrong_password(self):
        pssword_wrong = "1234"
        email = "tamara37@example.com"
        result_wrong = self.login.is_login(pssword_wrong, email)
        self.assertFalse(result_wrong["status"])
        self.assertEqual(result_wrong["message"], "Wrong password")

        self.database.remove("./test/db.sqlite3")


if __name__ == "__main__":
    unittest.main()
