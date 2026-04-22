import json
from typing import Any

from json_benchmarker import read_json, Item


def item_from_dict(data: dict[str, Any]) -> Item:
    """
    Transforms a dictionaty of items into an Item.

    Args:
        data: The dictionary
    Raises:
        ValueError: If the dictionary is of invalid format
    """
    name = data.pop("name")
    language = data.pop("language")
    id = data.pop("id")
    bio = data.pop("bio")
    version = data.pop("version")

    if any(item is None for item in [name, language, id, bio, version]):
        raise ValueError("Received invalid item")

    return Item(name, language, id, bio, version)


def read_with_rust() -> None:
    items = read_json("5MB.json")

    for item in items:
        print(item, type(item))
        print(item.name, item.language, item.id, item.bio, item.version, type(item.name))


def read_with_python() -> None:
    with open("5MB.json") as file:
        contents = file.read()
        data = json.loads(contents)
        print(data)

        items: list[Item] = []

        for item in data:
            print(item)
            items.append(item_from_dict(item))


def main():
    read_with_python()


if __name__ == "__main__":
    main()
