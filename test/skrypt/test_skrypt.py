import os
import subprocess
import unittest
from unittest.mock import patch
from io import StringIO

from script import Script


class TestSkrypt(unittest.TestCase):
    def setUp(self):
        self.script = Script("./test/skrypt/db.sqlite3")
        if not os.path.exists("./test/skrypt/db.sqlite3"):
            command = ["python3", "script.py", "create_database"]
            subprocess.run(command, capture_output=True, text=True)

    def test_valid_login(self):
        simulated_args = [
            "--login",
            "604020303",
            "--password",
            "6mKY!nP^+y",
            "print-all-accounts",
        ]
        with patch("sys.argv", ["script.py"] + simulated_args):
            with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
                self.script.main()
        expected_output = "79"
        self.assertIn(expected_output, mock_stdout.getvalue())

    def test_invalid_login(self):
        simulated_args = [
            "--login",
            "1233333333333333",
            "--password",
            "password",
            "print-all-accounts",
        ]
        with patch("sys.argv", ["script.py"] + simulated_args):
            with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
                self.script.main()
        expected_output = "InValid Login- Not Valid telephone number"
        self.assertIn(expected_output, mock_stdout.getvalue())

    def test_invalid_email(self):
        simulated_args = [
            "--login",
            "a.@pl",
            "--password",
            "password",
            "print-all-accounts",
        ]
        with patch("sys.argv", ["script.py"] + simulated_args):
            with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
                self.script.main()
        expected_output = "InValid Login- Not Valid email"
        self.assertIn(expected_output, mock_stdout.getvalue())

    def test_invalid_password(self):
        simulated_args = [
            "--login",
            "604020303",
            "--password",
            "password_wrong",
            "print-all-accounts",
        ]
        with patch("sys.argv", ["script.py"] + simulated_args):
            with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
                self.script.main()
        expected_output = "InValid Login- Wrong password"
        self.assertIn(expected_output, mock_stdout.getvalue())

    def test_user_not_found(self):
        simulated_args = [
            "--login",
            "123456789",
            "--password",
            "6mKY!nP^+y",
            "print-all-accounts",
        ]
        with patch("sys.argv", ["script.py"] + simulated_args):
            with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
                self.script.main()

        expected_output = "InValid Login- User Not Found"
        self.assertIn(expected_output, mock_stdout.getvalue())

    def test_no_access_to_command(self):
        simulated_args = [
            "--login",
            "203818382",
            "--password",
            "gk2VM$qk@S",
            "group-by-age",
        ]
        with patch("sys.argv", ["script.py"] + simulated_args):
            with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
                self.script.main()

        expected_output = "permission denied:  you are allow to use  print-children or find-similar-children-by-age "
        self.assertIn(expected_output, mock_stdout.getvalue())


if __name__ == "__main__":
    unittest.main()
