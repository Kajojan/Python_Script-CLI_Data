from main.db.db import DB
from main.db.data_loader import data_loader
import bcrypt


class Login:
    def __init__(self, db) -> None:
        self.dataBase = db
        self.load_manager = data_loader()

    def is_email(self, email):
        response = {}
        valid_email = self.load_manager.email([{"email": email}])
        if len(valid_email) == 0:
            response["status"] = False
            response["message"] = "Not Valid email"
            return response

        vali_email_value = valid_email[0]["email"]
        data = self.dataBase.get_data_by_email(vali_email_value)
        if data == None:
            response["status"] = False
            response["message"] = "User Not Found"
        else:
            response["status"] = True
            response["data"] = data
        return response

    def is_telephone_number(self, number):
        response = {}
        valid_number = self.load_manager.number([{"telephone_number": number}])
        if len(valid_number) == 0:
            response["status"] = False
            response["message"] = "Not Valid telephone number"
            return response

        vali_number_value = valid_number[0]["telephone_number"]
        data = self.dataBase.get_data_by_telefone_number(vali_number_value)

        if data == None:
            response["status"] = False
            response["message"] = "User Not Found"
        else:
            response["status"] = True
            response["data"] = data
        return response

    def is_login(self, password, number_emial):
        hash = self.dataBase.get_password(number_emial)
        if "@" in number_emial:
            response = self.is_email(number_emial)
        else:
            response = self.is_telephone_number(number_emial)

        if response["status"] == True:
            if bcrypt.checkpw(password.encode("utf-8"), hash):
                response["status"] = True
            else:
                response["status"] = False
                response["message"] = "Wrong password"

        return response
