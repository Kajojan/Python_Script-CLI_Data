from typing import Any

from main.db.file_type.type_interface import *
import xml.etree.ElementTree as ET


class Xml_Loader(Loder):
    def load(self, file) -> list[dict]:
        tree: Any = ET.parse(file)
        root: Any = tree.getroot()

        for child in root:
            row: dict = {}
            for sub_element in child:
                if sub_element.tag == "children":
                    row[sub_element.tag] = self.load_children(sub_element)
                else:
                    row[sub_element.tag] = sub_element.text
            self.data.append(row)

        return self.data

    def load_children(self, element) -> list[dict]:
        children_list = []
        for child in element:
            row: dict = {}
            for sub_element in child:
                row[sub_element.tag] = sub_element.text
            children_list.append(row)
        return children_list
