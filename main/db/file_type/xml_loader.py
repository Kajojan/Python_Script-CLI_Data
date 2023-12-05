from main.db.file_type.type_interface import *
import xml.etree.ElementTree as ET


class Xml_Loader(Loder):
    def load(self, file) -> object:
        tree = ET.parse(file)
        root = tree.getroot()

        for child in root:
            row = {}
            for sub_element in child:
                row[sub_element.tag] = sub_element.text
            self.data.append(row)

        return self.data
