from main.db.file_type.type_interface import *
import csv


class CSV_Loader(Loder):
    def load(self, file) -> object:
        with open(file, newline="") as csvfile:
            reader = csv.reader(csvfile, delimiter=";")
            headers = next(reader)
            for row in reader:
                data_row = {}
                for index, value in enumerate(row):
                    if headers[index] == "children" and len(value) > 0:
                        children_list = []
                        children_data = value.split(",")
                        for child_info in children_data:
                            child_name, child_age = child_info.strip().split(" ")
                            child_age = child_age.replace("(", "")
                            child_age = child_age.replace(")", "")
                            children_list.append(
                                {"name": child_name, "age": int(child_age)}
                            )
                        data_row[headers[index]] = children_list
                    else:
                        data_row[headers[index]] = value
                self.data.append(data_row)

        return self.data
