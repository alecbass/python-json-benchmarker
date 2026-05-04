from typing import Any

from json_benchmarker import Item


def item_from_dict(data: dict[str, Any]) -> Item:
    """
    Transforms a dictionaty of items into an Item.

    Args:
        data: The dictionary
    Raises:
        ValueError: If the dictionary is of invalid format, if the id field is not an integer
    """
    id = int(data.pop("id"))
    name = data.pop("name")
    description = data.pop("description")

    if any(item is None for item in [id, name, description]):
        raise ValueError("Received invalid item")

    return Item(id, name, description)
