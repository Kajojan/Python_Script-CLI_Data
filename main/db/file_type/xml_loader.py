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
                row[sub_element.tag] = sub_element.text
            self.data.append(row)

        return self.data
