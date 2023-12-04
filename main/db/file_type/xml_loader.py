from main.db.file_type.type_interface import *
import csv


class Xml_Loader(Loder):
    def load(self, file) -> object:
        with open(file, newline="") as csvfile:
            reader = csv.reader(csvfile, delimiter=";")
            headers = next(reader)
            for row in reader:
                data_row = {}
                for index, value in enumerate(row):
                    data_row[headers[index]] = value
                self.data.add(data_row)

        return self.data


