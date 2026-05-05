import json
from io import TextIOWrapper, open
from typing import Self

from json_benchmarker import Item

from utils import item_from_dict


class PythonChunkedReader:
    reader: TextIOWrapper
    limit: int
    _is_at_end: bool

    def __init__(self, reader: TextIOWrapper, limit: int) -> None:
        self.reader = reader
        self.limit = limit
        self._is_at_end = False

    def __next__(self) -> list[Item]:
        """
        Butchered implementation of https://github.com/ICRAR/ijson/blob/master/src/ijson/backends/python.py

        It reads and creates Item instances until it reaches the end of the file. Once that happens, the next call will
        raise StopIteration.

        This function is a war crime. It assumes that the JSON will be valid within and {} delimeters. It reads through the
        file one at a time which hopefully the buffered reader helps with, but still isn't ideal.

        If you saw the talk and read this code, message me and I'll buy you a coffee.
        """
        buffer = ""
        is_within_item = False
        items: list[Item] = []

        if self._is_at_end:
            raise StopIteration()

        while True:
            char = self.reader.read(1)

            if char == "":
                # Reached the end of the file
                self.reader.close()
                self._is_at_end = True
                return items

            if char == "{":
                is_within_item = True

            if not is_within_item:
                continue

            buffer += char

            if char == "}":
                is_within_item = False
                item_json = json.loads(buffer)
                item = item_from_dict(item_json)
                items.append(item)

                if len(items) == self.limit:
                    # Yield this chunk
                    return items

                buffer = ""

    @classmethod
    def create(cls, path: str, limit: int) -> Self:
        file = open(path, "r")
        return cls(file, limit)
