import json
from io import TextIOWrapper, open
from typing import Self

from json_benchmarker import Item

from utils import item_from_dict


class PythonChunkedReader:
    reader: TextIOWrapper
    limit: int

    def __init__(self, reader: TextIOWrapper, limit: int) -> None:
        self.reader = reader
        self.limit = limit

    def __next__(self) -> list[Item]:
        buffer = ""
        is_within_item = False
        items: list[Item] = []

        while True:
            char = self.reader.read(1)

            if char == "":
                # Reached the end of the file
                self.reader.close()
                raise StopIteration()

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
                    # TODO(alec): Yield items at this stage
                    return items

                buffer = ""

    @classmethod
    def create(cls, path: str, limit: int) -> Self:
        file = open(path, "r")
        return cls(file, limit)
