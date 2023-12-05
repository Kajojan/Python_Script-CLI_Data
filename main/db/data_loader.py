import os
import re
import sys

sys.path.append("./")
from pathlib import Path
from main.db.file_type import csv_loader

from main.db.file_type import json_loader

from main.db.file_type import xml_loader


class data_loader:
    def __init__(self) -> None:
        self.file_type = {
            ".csv": csv_loader.CSV_Loader(),
            ".json": json_loader.Json_Loader(),
            ".xml": xml_loader.Xml_Loader(),
        }

    def file_load(self, path: str):
        try:
            if Path(path).suffix in self.file_type:
                return self.file_type[Path(path).suffix].load(path)
            else:
                raise FileNotFoundError(f"Suffix not found: {path}")
        except FileNotFoundError:
            raise FileNotFoundError(f"File not found: {path}")
        except Exception as e:
            raise e

    def number(self, data: object):
        valid_data = []
        for index, user in enumerate(data):
            if user["telephone_number"] != "" or user["telephone_number"] != None:
                telephone_number = user["telephone_number"]
                telephone_number = telephone_number.replace(" ", "")

                if telephone_number.startswith("+"):
                    telephone_number = re.sub(r"\+(\d{2})", "+", telephone_number)
                elif telephone_number.startswith("0"):
                    telephone_number = telephone_number.lstrip("0")
                elif telephone_number.startswith("("):
                    telephone_number = re.sub(r"\([^)]*\)", "", telephone_number)

                telephone_number = re.sub(r"[^\w\s]", "", telephone_number)
                user["telephone_number"] = telephone_number

                if len(telephone_number) == 9:
                    valid_data.append(user)
        return valid_data

    def email(self, data: object):
        valid_data = []
        pattern = r"^[a-zA-Z0-9+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]{1,4}$"
        for index, user in enumerate(data):
            if re.match(pattern, user["email"]):
                valid_data.append(user)

        return valid_data

    def validation(self, data: object):
        numbers = self.number(data)
        email = self.email(numbers)
        return email
