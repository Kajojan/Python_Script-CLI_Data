from main.db.file_type.type_interface import *
import json


class Json_Loader(Loder):
    def load(self, file) -> object:
        with open(file) as jsonfile:
            self.data.append(json.load(jsonfile))
        return self.data

